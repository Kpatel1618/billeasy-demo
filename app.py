"""
Billeasy AI Native Tech Lead — Demo Build
GST E-Invoice Compliance Checker

What this does:
  1. Loads a small, hand-written rule set (rules/gst_einvoice_rules.md)
  2. Loads sample invoices (data/sample_invoices.json)
  3. For each invoice, asks an LLM to check it against the rules ONLY
     (grounded in-context — no vector DB, no RAG pipeline needed because
     the ruleset is small enough to fit directly in the prompt)
  4. Runs a second, deliberate self-check pass: the model reviews its own
     first answer against the rules again before we accept it. This is a
     simple two-step chain, not a multi-agent framework — enough process
     depth to catch obvious slip-ups without the complexity of an agent
     system I haven't built before.
  5. Writes a combined report to output/report.json and output/report.md

Requires: ANTHROPIC_API_KEY environment variable (free-tier / trial credits
are enough for this — no paid third-party tool is used).
"""

import os
import json
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Missing dependency. Run: pip install anthropic python-dotenv")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional — env var can be set directly instead

BASE_DIR = Path(__file__).parent
RULES_PATH = BASE_DIR / "rules" / "gst_einvoice_rules.md"
INVOICES_PATH = BASE_DIR / "data" / "sample_invoices.json"
OUTPUT_DIR = BASE_DIR / "output"
MODEL = "claude-sonnet-4-5"  # small/cheap+capable model is enough for this task

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env automatically


def load_rules() -> str:
    return RULES_PATH.read_text()


def load_invoices() -> list:
    return json.loads(INVOICES_PATH.read_text())


def build_system_prompt(rules_text: str) -> str:
    return f"""You are a GST e-invoice compliance checker for an eBilling platform.
Check the invoice you are given STRICTLY against the rules below. Do not use
any outside knowledge of GST rules beyond what is written here.

{rules_text}

Respond with ONLY valid JSON, no other text, in this exact shape:
{{
  "invoice_id": "...",
  "is_compliant": true/false,
  "issues": [
    {{"rule": "rule number + short name", "description": "...", "severity": "blocking|warning", "suggested_fix": "..."}}
  ]
}}
If there are no issues, return an empty issues list and is_compliant: true.
"""


def check_invoice(rules_text: str, invoice: dict) -> dict:
    system_prompt = build_system_prompt(rules_text)

    # --- Pass 1: initial check ---
    first_pass = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Invoice to check:\n{json.dumps(invoice, indent=2)}"}
        ],
    )
    first_result_text = first_pass.content[0].text.strip()

    # --- Pass 2: self-check — the model reviews its own first answer ---
    second_pass = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Invoice:\n{json.dumps(invoice, indent=2)}"},
            {"role": "assistant", "content": first_result_text},
            {"role": "user", "content": (
                "Re-check your own analysis above against the rules one more time. "
                "Correct anything you missed or got wrong, including arithmetic. "
                "Respond with ONLY the corrected JSON in the same shape, nothing else."
            )},
        ],
    )
    final_text = second_pass.content[0].text.strip()

    return parse_json_safely(final_text, invoice.get("invoice_id", "UNKNOWN"))


def parse_json_safely(text: str, invoice_id: str) -> dict:
    # Models occasionally wrap JSON in ```json fences — strip if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "invoice_id": invoice_id,
            "is_compliant": None,
            "issues": [],
            "raw_output": text,
            "parse_error": True,
        }


def write_reports(results: list):
    OUTPUT_DIR.mkdir(exist_ok=True)

    (OUTPUT_DIR / "report.json").write_text(json.dumps(results, indent=2))

    lines = ["# Billeasy GST E-Invoice Compliance Report\n"]
    compliant_count = sum(1 for r in results if r.get("is_compliant") is True)
    lines.append(f"**Summary:** {compliant_count}/{len(results)} invoices fully compliant.\n")

    for r in results:
        status = "✅ Compliant" if r.get("is_compliant") else "❌ Issues found"
        lines.append(f"## {r.get('invoice_id', 'UNKNOWN')} — {status}\n")
        issues = r.get("issues", [])
        if not issues:
            lines.append("No issues found.\n")
        else:
            for issue in issues:
                lines.append(
                    f"- **[{issue.get('severity', '?').upper()}] {issue.get('rule', '')}** — "
                    f"{issue.get('description', '')}\n  - Fix: {issue.get('suggested_fix', '')}"
                )
        lines.append("")

    (OUTPUT_DIR / "report.md").write_text("\n".join(lines))


def main():
    rules_text = load_rules()
    invoices = load_invoices()

    print(f"Loaded {len(invoices)} sample invoices. Checking each against the rule set...\n")

    results = []
    for invoice in invoices:
        print(f"Checking {invoice['invoice_id']}...")
        result = check_invoice(rules_text, invoice)
        results.append(result)
        status = "COMPLIANT" if result.get("is_compliant") else "ISSUES FOUND"
        print(f"  -> {status} ({len(result.get('issues', []))} issue(s))\n")

    write_reports(results)
    print(f"Done. Reports written to {OUTPUT_DIR}/report.md and {OUTPUT_DIR}/report.json")


if __name__ == "__main__":
    main()
