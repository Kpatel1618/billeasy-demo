# Billeasy GST E-Invoice Compliance Checker

A small AI tool that checks sample GST e-invoices against a written rule
set and flags issues in plain language — built for Billeasy's "build
anything" AI-native assessment.

## Why this, why this small
- Billeasy is an eBilling/eCommerce/POS company — GST e-invoice compliance
  is a real, recurring problem for any merchant on their platform.
- No vector database, no agent framework, no paid tools: the rule set is
  small enough to sit directly in the prompt, so a single well-structured
  LLM call (plus one self-check pass) is enough. Keeping it this simple was
  itself a deliberate decision — worth a line in the write-up.

## What's in here
```
billeasy-demo/
├── data/sample_invoices.json      8 mock invoices — mix of clean and flawed
├── rules/gst_einvoice_rules.md    the compliance rules the AI checks against
├── app.py                         the script: load → check → self-check → report
├── requirements.txt
├── .env.example
├── output/                        report.json + report.md land here after running
└── WRITEUP_TEMPLATE.md            scaffold for the submission write-up
```

## Setup (≈15 min)
1. Get a **free** API key from Google AI Studio: https://aistudio.google.com/apikey
   — no credit card, no purchase required, generous free daily quota.
2. `pip install -r requirements.txt` (uses the current `google-genai` SDK)
3. Copy `.env.example` to `.env` and paste your key in as
   `GOOGLE_API_KEY=...`.

## Run it (≈2 min)
```
python3 app.py
```
This checks all 8 sample invoices and writes `output/report.md` and
`output/report.json`.

## Suggested 2–3 hour build plan
| Time | Task |
|---|---|
| 0:00–0:15 | Read through `sample_invoices.json` and `gst_einvoice_rules.md` so you know exactly what's already built and why |
| 0:15–0:30 | Get your API key set up, install deps, run `python3 app.py` once as-is to confirm it works end to end |
| 0:30–1:00 | Read the actual output in `output/report.md` — does it catch the deliberate errors in invoices 1002–1005, 1007? Note anything it got wrong or missed — this is real material for the write-up's "surprises" section |
| 1:00–1:30 | Make one deliberate change yourself and re-run — e.g. edit `rules/gst_einvoice_rules.md` to add a rule, or edit the system prompt in `app.py`, and see how the output changes. This gives you a genuine "I changed X because Y" story |
| 1:30–2:00 | (Optional, if time allows) Wrap `app.py`'s output in a tiny Streamlit UI (`pip install streamlit`) so the demo looks like a product, not a script |
| 2:00–2:30 | Write the submission write-up using `WRITEUP_TEMPLATE.md`, filling in your real observations from the run |
| 2:30–3:00 | Buffer / polish / re-run if you tweaked anything |

## Notes on the design decisions (useful for your write-up)
- **In-context rules over RAG**: with ~10 rules, retrieval would add
  complexity without adding value. If the ruleset grew to hundreds of
  rules, that's the point I'd introduce a retrieval step.
- **Two-pass self-check instead of an agent**: rather than reaching for an
  agent framework I've never used, I used a simple two-message chain where
  the model reviews its own first answer. It's the smallest structure that
  still catches the model's own mistakes (especially arithmetic).
- **Strict JSON output**: forcing structured output makes the results easy
  to render as a report and easy to test — a plain-language answer would be
  harder to verify programmatically.
