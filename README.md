# Billeasy GST E-Invoice Compliance Checker

A small AI tool that checks sample GST e-invoices against a written rule set and flags issues in plain language — built for Billeasy's "build anything" AI-native assessment.

## Why this, why this small

Billeasy is an eBilling/eCommerce/POS company — GST e-invoice compliance is a real, recurring problem for merchants using such platforms.

No vector database, no agent framework, and no paid tools: the rule set is small enough to sit directly in the prompt, so a single well-structured LLM call plus one self-check pass is enough.

Keeping the solution simple was a deliberate design decision. If the ruleset grows significantly, the architecture can evolve toward RAG or a more sophisticated agentic approach.

## What's in here

```text
billeasy-demo/
├── data/
│   └── sample_invoices.json       # 8 mock invoices — mix of clean and flawed
├── rules/
│   └── gst_einvoice_rules.md      # Compliance rules checked by the AI
├── app.py                         # Load → check → self-check → report
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── output/                        # report.json + report.md generated here
└── WRITEUP_TEMPLATE.md            # Submission write-up scaffold
```

## Technology

- Python 3
- Groq API
- Llama model via Groq
- JSON-based invoice input
- Markdown-based GST compliance rules
- Structured JSON output
- Two-pass AI validation/self-check
- `python-dotenv` for environment variable management

## Prerequisites

Before running the application locally, make sure you have:

- Python 3.9+ installed
- Git installed
- A free Groq API key

Create a Groq API key from the [Groq Console](https://console.groq.com/keys).

> **Security:** Never commit your actual API key to GitHub. Store it only in your local `.env` file. The `.env` file is excluded through `.gitignore`.

## Clone the Repository

Open Command Prompt, PowerShell, Terminal, or Git Bash and run:

```bash
git clone https://github.com/Kpatel1618/billeasy-demo.git
cd billeasy-demo
```

Verify the repository contents.

### Windows

```powershell
dir
```

### macOS/Linux

```bash
ls
```

## Create a Virtual Environment

Creating a virtual environment keeps the project's dependencies isolated.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, you should see:

```text
(.venv)
```

at the beginning of your terminal prompt.

## Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configure the Groq API Key

Copy the example environment file.

### Windows

```powershell
copy .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

For example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

Do not commit the `.env` file to GitHub.

The repository contains `.env.example` only as a safe template.

## Run the Application

Once the environment is configured, run:

```bash
python app.py
```

The application will:

1. Load the sample GST e-invoices.
2. Load the GST e-invoice compliance rules.
3. Send the relevant information to the Groq-powered LLM.
4. Check each invoice for compliance issues.
5. Perform a second self-check pass.
6. Generate structured results.
7. Write the final reports to the `output/` directory.

After execution, the following files will be generated:

```text
output/
├── report.json
└── report.md
```

Open `output/report.md` to review the human-readable compliance report.

## Quick Start

For an experienced developer, the complete setup is:

```bash
git clone https://github.com/Kpatel1618/billeasy-demo.git
cd billeasy-demo

python -m venv .venv
```

Activate the environment:

### Windows

```powershell
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt

# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Add your Groq API key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Then run:

```bash
python app.py
```

## Suggested 2–3 Hour Build Plan

| Time | Task |
|---|---|
| 0:00–0:15 | Read `sample_invoices.json` and `gst_einvoice_rules.md` to understand the existing solution and design |
| 0:15–0:30 | Configure the Groq API key, install dependencies, and run `python app.py` to confirm the end-to-end flow |
| 0:30–1:00 | Review `output/report.md` and verify whether the AI catches the deliberate errors in invoices 1002–1005 and 1007 |
| 1:00–1:30 | Make one deliberate change — for example, add a rule to `gst_einvoice_rules.md` or modify the system prompt in `app.py` — and compare the output |
| 1:30–2:00 | Optional: Wrap the application in a small Streamlit UI to make the demo more product-like |
| 2:00–2:30 | Complete the submission write-up using `WRITEUP_TEMPLATE.md` |
| 2:30–3:00 | Buffer for testing, refinement, and final cleanup |

## Design Decisions

### In-context Rules Instead of RAG

The current ruleset contains only a small number of rules, so retrieval would introduce additional complexity without providing significant value.

The rules are therefore supplied directly to the LLM as context.

If the ruleset grows to hundreds or thousands of rules, a retrieval-based architecture would become more appropriate.

### Two-pass Self-check Instead of an Agent

Rather than introducing an agent framework unnecessarily, the solution uses a simple two-pass approach:

**Pass 1:** Analyze the invoice against the GST rules.

**Pass 2:** Review the first response and identify potential mistakes or inconsistencies.

This provides an additional validation layer while keeping the architecture simple and transparent.

### Strict JSON Output

The LLM is instructed to return structured JSON.

This makes the results:

- Easier to validate
- Easier to process programmatically
- Easier to convert into Markdown reports
- More consistent than relying on free-form text

## Example Workflow

```text
Sample GST Invoice
        │
        ▼
Load GST Compliance Rules
        │
        ▼
Groq / LLM Analysis
        │
        ▼
Compliance Result
        │
        ▼
AI Self-Check
        │
        ▼
Structured JSON
        │
        ├──────────────► report.json
        │
        └──────────────► report.md
```

## Security

The project uses environment variables for API credentials.

```text
.env                  → Local secret — DO NOT COMMIT
.env.example          → Safe template — COMMIT
```

The expected environment variable is:

```env
GROQ_API_KEY=your_groq_api_key_here
```

If an API key is accidentally committed, revoke/rotate the key immediately and remove the secret from Git history before pushing the repository.

## Future Enhancements

Potential next steps include:

- Streamlit-based user interface
- Upload GST invoice JSON directly
- Support for PDF invoice extraction
- RAG-based rules retrieval for larger rule sets
- Automated GST rule/version management
- Confidence scoring
- Audit trail for compliance decisions
- Human review workflow for ambiguous cases
- Automated test suite for compliance scenarios
- Production deployment using Azure/AWS

## License

This project is created as a demonstration/assessment project for Billeasy and is not intended to provide legal or tax advice.

## Updating the README on GitHub

After replacing your existing `README.md` with this file, save it and run:

```bash
git status
git add README.md
git commit -m "Update README with Groq setup and local run instructions"
git push origin main
```

You can verify the change with:

```bash
git log --oneline -1
```

You should see:

```text
Update README with Groq setup and local run instructions
```

> **Important:** Do not run `git add .` for this change unless you've checked that `.env` is ignored. The safest command here is specifically:
>
> ```bash
> git add README.md
> ```
>
> This ensures your local `.env` file is not accidentally included in the commit.
