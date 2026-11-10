# Job Search AI

<p align="center">
  <img src="assets/readme/hero.svg" alt="Job Search AI - Agentic Job Application Framework" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Bhuvantejakomera/Job_search_AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-2A9D8F?style=flat" alt="MIT license"></a>
  &nbsp;
  <a href="https://deepmind.google/technologies/antigravity"><img src="https://img.shields.io/badge/Agent-Google_Antigravity-4285F4?style=flat&logo=google" alt="Google Antigravity"></a>
  &nbsp;
  <a href="https://claude.com/claude-code"><img src="https://img.shields.io/badge/Agent-Claude_Code-D97706?style=flat" alt="Claude Code"></a>
  &nbsp;
  <a href="https://bun.sh"><img src="https://img.shields.io/badge/Runtime-Bun-fbf0df?style=flat&logo=bun&logoColor=black" alt="Bun"></a>
  &nbsp;
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></a>
</p>

<p align="center">
  An autonomous, agentic job search and application engine built for <b>Google Antigravity, Claude Code, Cursor, Codex, and the Terminal</b>.<br>
  Search live job boards, evaluate role fit, tailor ATS-optimized resumes and cover letters in LaTeX, compile clean PDFs instantly, and prep for interviews.
</p>

<p align="center">
  <a href="#core-capabilities"><b>Capabilities</b></a>
  &nbsp;&bull;&nbsp;
  <a href="#quick-start"><b>Quick Start</b></a>
  &nbsp;&bull;&nbsp;
  <a href="#terminal-usage"><b>Terminal Usage</b></a>
  &nbsp;&bull;&nbsp;
  <a href="#agent-workflows"><b>Agent Workflows</b></a>
  &nbsp;&bull;&nbsp;
  <a href="#command-reference"><b>Commands</b></a>
  &nbsp;&bull;&nbsp;
  <a href="#project-structure"><b>Structure</b></a>
  &nbsp;&bull;&nbsp;
  <a href="#privacy--security"><b>Privacy & Security</b></a>
</p>

---

## Core Capabilities

- 🔍 **Live Multi-Portal Search:** Zero-login search across **LinkedIn** (`jobs-guest` endpoints), **Freehire** (aggregating 50+ ATS platforms like Greenhouse, Lever, Ashby, Workday), and **Indeed**.
- 🎯 **Intelligent Fit Assessment:** Evaluates role requirements against your core tech stack, experience level, and personal deal-breakers before you spend time applying.
- 📄 **ATS-Optimized Resumes & Cover Letters:** Generates tailored LaTeX source code (`moderncv` banking style and custom `cover.cls`) customized to the exact keywords of each job posting.
- ⚡ **Instant PDF Compilation:** Integrated PDF builder (`tools/build_pdf.py`) utilizing standalone Tectonic or system TeX engines—**no heavy 5GB+ TeX distribution required**.
- 🔄 **Deduplication & Pipeline Tracking:** Persistent deduplication prevents duplicate applications, while `job_search_tracker.csv` manages your active application funnel.
- 🤝 **Automated Referral Discovery:** Auto-generates targeted LinkedIn recruiter and peer-search links for every promising job match.
- 🎙️ **Stage-Specific Interview Preparation:** Generates STAR-method talking points, reverse-interview questions, and roleplay mock sessions based on your actual submitted application.

---

## Quick Start

### 1. Prerequisites

| Tool | Purpose | Installation |
|---|---|---|
| **Python 3.9+** | State management, deduplication, and PDF build tools | Pre-installed on macOS/Linux |
| **[Bun](https://bun.sh)** | Fast TypeScript runtime for portal search CLIs | `curl -fsSL https://bun.sh/install \| bash` |
| **Agent CLI** *(Optional)* | For conversational autonomous workflows | [Google Antigravity](https://deepmind.google/technologies/antigravity) or [Claude Code](https://claude.com/claude-code) |

### 2. Clone the Repository

```bash
git clone https://github.com/Bhuvantejakomera/Job_search_AI.git
cd Job_search_AI
```

### 3. Configure Your Profile

You can configure your candidate background in one of two ways:

- **Interactive Setup (Agent Mode):** In Antigravity or Claude Code chat, type `/setup` to import an existing CV or complete a guided onboarding interview.
- **Manual Setup:** Fill in your details in [`CLAUDE.md`](CLAUDE.md) and [`.claude/skills/job-application-assistant/01-candidate-profile.md`](.claude/skills/job-application-assistant/01-candidate-profile.md). Replace the `[PLACEHOLDER]` tokens with your identity, education, experience, technical skills, and target preferences.

---

## Terminal Usage

You can search live portals, compile LaTeX resumes, and manage job states directly in your terminal without opening an AI chat.

### 1. Search Live Jobs

#### LinkedIn Search CLI (`linkedin-search`)
Query LinkedIn's public job endpoints by role, experience keywords, and location:
```bash
# Search Generative AI junior/associate roles in India (last 14 days)
bun run .agents/skills/linkedin-search/cli/src/cli.ts search \
  --location "India" \
  --query "Generative AI (Junior OR Intern OR Associate OR Fresher)" \
  --jobage 14 \
  --limit 10 \
  --format table

# Search Remote AI / LLM Engineer positions
bun run .agents/skills/linkedin-search/cli/src/cli.ts search \
  --location "Remote" \
  --query "LLM Engineer" \
  --jobage 14 \
  --limit 10
```

#### Freehire ATS Aggregator CLI (`freehire-search`)
Query real-time postings crawled from Greenhouse, Lever, Workday, etc., with structured seniority facets:
```bash
# Search Junior AI / Machine Learning roles in India
bun run .agents/skills/freehire-search/cli/src/cli.ts search \
  -q 'title:"AI" OR title:"Machine Learning"' \
  --country IN \
  --seniority junior \
  --jobage 14 \
  --limit 15 \
  --format table

# Search Computer Vision & PyTorch listings
bun run .agents/skills/freehire-search/cli/src/cli.ts search \
  -q "Vision Transformer PyTorch" \
  --format table
```

### 2. Compile Resumes and Cover Letters to PDF

Compile LaTeX documents directly to PDF in 1–2 seconds:
```bash
# Compile a specific CV
python3 tools/build_pdf.py cv/main_<company>_<role>.tex

# Compile a specific cover letter
python3 tools/build_pdf.py cover_letters/cover_<company>_<role>.tex

# Batch compile all CVs and cover letters in the workspace
python3 tools/build_pdf.py --all
```
*Generated PDFs land beside their `.tex` source and are automatically archived into `documents/applications/<company>/`.*

### 3. Deduplication & State Helpers

```bash
# Generate a canonical deduplication key for a job
python3 tools/job_key.py --company "Company Name" --title "Role Title" --url "https://posting.url"

# Filter raw candidate JSON against seen_jobs.json and job_search_tracker.csv
python3 tools/scrape_state.py candidates --results candidates.json

# Fetch a webpage safely with browser headers and robots.txt check
python3 tools/fetch_page.py "<URL>" --text --max-chars 3000
```

---

## Agent Workflows

When using an AI coding agent like **Google Antigravity** or **Claude Code**, the framework operates as an intelligent pair programmer managing your entire job hunt.

```
       ┌──────────┐
       │  /scrape │ ──► Discovers live roles & scores fit
       └────┬─────┘
            ▼
       ┌──────────┐
       │  /apply  │ ──► Tailors CV & cover letter, compiles PDF & ATS check
       └────┬─────┘
            ▼
       ┌───────────┐
       │/interview │ ──► Generates STAR talking points & mock Q&A
       └────┬──────┘
            ▼
       ┌───────────┐
       │  /outcome │ ──► Archives materials & updates tracker
       └───────────┘
```

1. **Find New Positions:**
   Type `/scrape` or `"Find new jobs"`. The agent searches configured portals, deduplicates against past runs, runs a quick fit check, and surfaces a prioritized shortlist with recruiter outreach links.
2. **Apply to a Listing:**
   Type `/apply <URL>` (or paste job description text). The agent evaluates fit against your profile, crafts a targeted CV and cover letter, runs a secondary review, compiles the PDF, and verifies ATS text readability.
3. **Prepare for Interviews:**
   Type `/interview` to generate interview battle-cards, company background research, and practice behavioral STAR questions for an upcoming conversation.

---

## Command Reference

| Command | Description |
|---|---|
| **`/setup`** | Builds or updates your candidate profile from documents, a pasted CV, or an interview. |
| **`/scrape`** | Searches job portals, removes duplicates, and presents matches sorted by fit. |
| **`/apply`** | Evaluates fit, then drafts, reviews, compiles, and verifies tailored CV and cover letter PDFs. |
| **`/rank`** | Batch-scores scraped postings against your profile rubric to produce a ranked shortlist. |
| **`/interview`** | Builds a stage-specific prep pack and conducts mock interview simulations. |
| **`/outcome`** | Records interview stages, offers, or rejections, and archives submitted dossiers. |
| **`/upskill`** | Identifies skill gaps across target postings and generates a personalized study roadmap. |
| **`/html-report`** | Generates an offline, interactive HTML analytics dashboard from your application tracker. |
| **`/gmail-sync`** | Auto-detects status updates and interview invitations from your email. |
| **`/notion-sync`** | Publishes a read-only mirror of your application pipeline to a Notion database. |
| **`/add-portal`** | Scaffolds a new portal search CLI skill for an additional job board in your region. |

---

## Project Structure

```
Job_search_AI/
├── AGENTS.md                          # Thin-pointer guidelines for multi-agent support
├── CLAUDE.md                          # Canonical candidate profile & workflow rules
├── README.md                          # Framework documentation
├── .agents/skills/                    # Portable job portal CLI tools
│   ├── linkedin-search/               # LinkedIn jobs-guest search skill
│   ├── freehire-search/               # freehire.me REST API search skill (50+ ATS platforms)
│   ├── indeed-search/                 # Indeed search skill
│   ├── jobbank-search/                # Akademikernes Jobbank
│   ├── jobdanmark-search/             # Jobdanmark
│   ├── jobindex-search/               # Jobindex
│   └── jobnet-search/                 # Jobnet (STAR)
├── .claude/
│   ├── commands/                      # Slash command definitions (/apply, /scrape, /rank, etc.)
│   └── skills/
│       ├── job-application-assistant/ # Profiling, fit evaluation rubric, CV/letter guidelines
│       ├── job-scraper/               # Search orchestration and search queries
│       └── upskill/                   # Skill gap analysis engine
├── cv/                                # ModernCV LaTeX source files
│   └── main_example.tex               # Reference CV template
├── cover_letters/                     # Cover letter LaTeX source files
│   ├── cover.cls                      # Custom cover letter LaTeX document class
│   ├── cover_example.tex              # Reference cover letter template
│   └── OpenFonts/                     # Bundled Lato & Raleway typography
├── tools/                             # Automation and verification utilities
│   ├── build_pdf.py                   # Automated LaTeX-to-PDF compilation script
│   ├── fetch_page.py                  # Webpage fetcher with robots.txt gate and browser headers
│   ├── job_key.py                     # Canonical posting key and deduplication hasher
│   ├── scrape_state.py                # Scraper candidate selection and atomic storage
│   ├── rank_state.py                  # Batch ranking helper
│   ├── verify_pdf.py                  # ATS extraction & page count validator
│   └── install_portal_clis.py         # Automated CLI dependency installer
└── job_search_tracker.csv             # Application tracking spreadsheet (locally ignored)
```

---

## Privacy & Security

This repository is engineered to protect your personal privacy:

- **Strict Data Ignorance:** All generated application CVs (`cv/main_*.tex`), cover letters (`cover_letters/cover_*.tex`), application dossiers (`documents/applications/`), search history (`job_scraper/seen_jobs.json`), and tracker logs (`job_search_tracker.csv`) are automatically excluded in [`.gitignore`](.gitignore).
- **Public Fork Safe:** Your personal contact information, phone numbers, and private emails remain local to your machine.
- **Untrusted Input Defense:** External job postings and fetched webpage text pass through an integrity gate before ingestion to defend against prompt injection or malicious instructions.

---

## License

This project is licensed under the [MIT License](LICENSE).

<p align="center">
  <sub>Built for developers and engineers streamlining their career growth with agentic AI.</sub>
</p>
