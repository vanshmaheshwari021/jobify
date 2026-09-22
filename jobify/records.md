# Project Audit & Modification Records

## Project Overview
- **Repository**: `https://github.com/perryvegehan/PWP_jobhunt.git`
- **Description**: Python CLI job-search pipeline (scans Greenhouse, Lever, Ashby ATS boards → prefilters → LLM screens & drafts → generates HTML digest → sends email via SMTP).

---

## 1. Original Files in Repository
When the repository was cloned, it contained the following structure:
- `jobhunt/`: Core Python package (pipeline logic, scrapers, LLM screeners, digest generator, CLI parser).
- `config.yaml`: Pre-filter regex rules, score threshold (7.0), max per digest (5), file paths.
- `companies.yaml`: ATS board slugs (Greenhouse, Lever, Ashby).
- `.env.example`: Template for `LLM_PROVIDER`, `GEMINI_API_KEY`, `SCREEN_MODEL`, `DRAFT_MODEL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `MAIL_TO`.
- `.github/workflows/daily.yml`: GitHub Actions daily automated workflow triggered by cron (`"30 0 * * 1-5"` = 06:00 IST / 00:30 UTC weekdays).
- `requirements.txt`: Python package dependencies (`requests`, `PyYAML`, `anthropic`, `pydantic`, `pytest`, etc.).
- `README.md`: System overview, CLI command usage, architecture diagram, environment variables reference.
- `SETUP.md`: Step-by-step installation and configuration guide.
- `profile.example.json`: Sample resume profile schema.

---

## 2. Files Created & Environment Setup
The following environment setup and files were created locally:

### Environment & Dependencies
- Created Python 3.11 Virtual Environment at `.venv/`.
- Installed all required packages from `requirements.txt`.
- Verified installation with dry run: `python -m jobhunt run --mock --scorer keyword`.

### Generated Configuration Files
- `.env`: Created local environment configuration with `LLM_PROVIDER=gemini`, `GEMINI_API_KEY`, models, and SMTP defaults.
- `out/digest.html`: Generated mock HTML digest output from pipeline runs.
- `out/tracker.csv`: Tracking history CSV file.

### Web Setup Console App
- `index.html` (in workspace root) and `PWP_jobhunt/index.html`: Self-contained standalone client-side setup and automation console for configuring `.env`, `config.yaml`, GitHub Actions `cron:`, and Secrets checklist (Jobify Automation Console).

---

## 3. Web Console Features Implemented
- **Email Delivery Form**: Gmail address, `MAIL_TO` override toggle, Gmail App Password input with 16-character validation warning.
- **LLM Engine Select**: Providers (`Anthropic`, `Google Gemini`, `Groq`, `OpenAI-compatible`, `Ollama`, `Custom`), API Key input, Screening & Drafting model text inputs with `<datalist>` suggestions, `LLM_BASE_URL` toggle, and split provider overrides (`SCREEN_PROVIDER` / `DRAFT_PROVIDER`).
- **Filter Rules (`config.yaml`)**: Tag/chip inputs for `include_titles`, `exclude_titles`, and `locations` with preset chips, custom preset saver (`localStorage` backed), `allow_remote` toggle, `score_threshold` (default 7.0), `max_per_digest` (default 5), and `max_age_days` (with "no limit" checkbox for `null`).
- **Automation Scheduler**: 12-hour IST time control (Hour 1..12, Minute 0..59, AM/PM toggle) + weekday checkboxes (Mon-Sun).
- **Exact IST to UTC Cron Logic**: Computes 24h IST time, subtracts 330 minutes for UTC, detects day rollback (`dayShiftedBack`), shifts UTC cron weekdays accordingly (Sun=0..Sat=6), formats `{utcMin} {utcHour} * * {dayList}`, and renders a human check explanation line.
- **Outputs & Checklist**: Real-time live updating code blocks for `.env`, `config.yaml filters:`, `.github/workflows/daily.yml` cron line, and plain GitHub Actions setup checklist with copy-to-clipboard functionality.
- **Jobify UI System Design**: Updated branding to `Jobify` with an `antigravity-design-expert` Beach Theme overhaul featuring warm golden sand (`#ffb703`), ocean turquoise (`#06b6d4`), and coral sunset (`#ff7043`) accents, translucent coastal glassmorphism surfaces, spatial backdrop orbs, floating error popups, and a direct link to `https://myaccount.google.com/apppasswords`.
- **Target Companies (`companies.yaml`) Generator**: Auto-parses pasted ATS board URLs (`boards.greenhouse.io/<slug>`, `jobs.lever.co/<slug>`, `jobs.ashbyhq.com/<slug>`) or bare slugs into valid `{ats, slug, name}` tuples with preset board chips and live `companies.yaml` code output.
- **Resume Upload & Profile JSON**: Drag-and-drop file uploader for resumes (`.pdf`, `.txt`, `.md`, `.json`) with client-side text parsing and live generating output block for the `PROFILE_JSON` GitHub Action secret.

---

## 4. Custom Learned Skills
- **`antigravity-design-expert`**: Created at `.agents/skills/antigravity-design-expert/SKILL.md`. Configures guidelines for UI/UX engineering, spatial depth, glassmorphism, GSAP motion design, and performance constraints.

---

## 5. Current Status
- Server active on `http://localhost:8000/index.html`.
- All CLI tools and configuration files verified and functional.

