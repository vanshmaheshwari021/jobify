"""Tests for guaranteed daily email delivery on all exit paths in cmd_run()."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jobhunt import cli, mailer


def test_cmd_run_sends_email_when_no_new_jobs(tmp_path, monkeypatch):
    """When no new jobs match or remain unseen, cmd_run with --send must call mailer.send."""
    prof_file = tmp_path / "profile.json"
    prof_file.write_text('{"target_titles":["Engineer"]}', encoding="utf-8")

    config_content = f"""
filters:
  include_titles: ['.*']
  exclude_titles: []
score_threshold: 7.0
max_per_digest: 5
companies_file: companies.yaml
profile_file: {prof_file}
seen_file: {tmp_path / 'seen.json'}
digest_file: {tmp_path / 'digest.html'}
"""
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(config_content, encoding="utf-8")

    sent_calls = []
    def mock_send(subject, body):
        sent_calls.append((subject, body))

    monkeypatch.setattr(mailer, "send", mock_send)

    class Args:
        config = str(cfg_file)
        mock = True
        scorer = "keyword"
        no_draft = True
        send = True
        limit = None

    args = Args()

    # First run: should find mock jobs and send email
    ret1 = cli.cmd_run(args)
    assert ret1 == 0
    assert len(sent_calls) == 1

    # Second run: all jobs are now seen, 0 new jobs remain. Must STILL send email!
    sent_calls.clear()
    ret2 = cli.cmd_run(args)
    assert ret2 == 0
    assert len(sent_calls) == 1
    assert "No new matches today" in sent_calls[0][0]


def test_cmd_run_sends_email_when_empty_companies(tmp_path, monkeypatch):
    """When companies.yaml has no entries, cmd_run with --send must send an error notice email."""
    prof_file = tmp_path / "profile.json"
    prof_file.write_text('{"target_titles":["Engineer"]}', encoding="utf-8")

    comp_file = tmp_path / "companies.yaml"
    comp_file.write_text("companies: []", encoding="utf-8")
    
    cfg_file = tmp_path / "config.yaml"
    config_content = f"""
companies_file: {comp_file}
profile_file: {prof_file}
seen_file: {tmp_path / 'seen.json'}
"""
    cfg_file.write_text(config_content, encoding="utf-8")

    sent_calls = []
    def mock_send(subject, body):
        sent_calls.append((subject, body))

    monkeypatch.setattr(mailer, "send", mock_send)

    class Args:
        config = str(cfg_file)
        mock = False
        scorer = "keyword"
        no_draft = True
        send = True
        limit = None

    ret = cli.cmd_run(Args())
    assert ret == 1
    assert len(sent_calls) == 1
    assert "Nothing scanned today" in sent_calls[0][0]


def test_cmd_run_sends_email_when_screening_fails(tmp_path, monkeypatch):
    """When LLM screening fails for all batches, cmd_run with --send must send an alert email."""
    prof_file = tmp_path / "profile.json"
    prof_file.write_text('{"target_titles":["Engineer"]}', encoding="utf-8")

    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(f"""
filters: {{include_titles: ['.*']}}
score_threshold: 7.0
profile_file: {prof_file}
seen_file: {tmp_path / 'seen.json'}
""", encoding="utf-8")

    sent_calls = []
    def mock_send(subject, body):
        sent_calls.append((subject, body))

    monkeypatch.setattr(mailer, "send", mock_send)

    # Mock llm.screen to leave all job scores as None (simulating batch failure)
    def mock_screen(jobs, profile, **kwargs):
        for j in jobs:
            j.score = None

    class MockProvider:
        name = "mock"

    monkeypatch.setattr("jobhunt.llm.screen", mock_screen)
    monkeypatch.setattr("jobhunt.cli.resolve", lambda stage: (MockProvider(), "mock-model"))

    class Args:
        config = str(cfg_file)
        mock = True
        scorer = "llm"
        no_draft = True
        send = True
        limit = None

    ret = cli.cmd_run(Args())
    assert ret == 1
    assert len(sent_calls) == 1
    assert "Screening failed" in sent_calls[0][0]
