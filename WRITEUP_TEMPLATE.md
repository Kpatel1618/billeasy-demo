# Submission Write-up — GST E-Invoice Compliance Checker

Fill this in with your real observations after running the tool. Keep it
honest — specific, small details are more convincing than polished claims.

## What I built and why

I built a small AI tool that checks GST e-invoices against a written
compliance rule set and flags issues in plain language, along with a
suggested fix per issue.

I chose this over a generic AI demo because Billeasy's core product is
eBilling, and GST e-invoice errors are a real, recurring problem for any
merchant issuing B2B invoices in India — [add a sentence here on any
specific experience you've had with invoicing/compliance pain points, even
adjacent ones from your banking/regulatory background].

## AI tools, models, and their role

- **[Model name, e.g. Claude Sonnet]** — used for the core compliance
  check: given the invoice and the rule set, it identifies violations,
  severity, and suggested fixes.
- **[Model name]** — also used for a second "self-check" pass, reviewing
  its own first answer against the rules before the result is accepted.
- **[If used] Claude/ChatGPT during my own build process** — I used it to
  [e.g. "draft the initial GST rule list, which I then reviewed and
  trimmed myself" / "help me structure the prompt" / "debug the JSON
  parsing"]. Be specific and honest here — this is part of what they're
  evaluating.

## Key moments where AI shaped my decisions

- [Fill in from your actual run] e.g. "I originally planned to use a
  vector database to look up relevant rules per invoice, but once I wrote
  the rule set down, it was under 500 words — small enough to put directly
  in the prompt. That changed my architecture from a RAG pipeline to a
  single grounded prompt."
- [Fill in] e.g. "The first version of the prompt let the model respond in
  free text, which made the results hard to check. Switching to a strict
  JSON schema was an AI-influenced structural decision — it forced the
  compliance logic to be explicit rather than buried in prose."
- [Fill in] e.g. "Adding the self-check pass was a direct response to
  seeing the model make an arithmetic mistake on the first pass for
  invoice 1004 — I decided a second review step was worth the extra API
  call rather than trusting the first answer."

## Where AI surprised me or changed my approach

[This section only works if you actually run it and observe something —
don't fabricate it. Things worth watching for:]
- Did the self-check pass actually catch something the first pass missed?
- Did the model flag something you didn't expect (e.g. the GST-rate sanity
  check on invoice 1007, which is a "possible issue" rather than a hard
  rule) — did it handle that nuance well or overreact?
- Did it ever invent an issue not covered by the rules, despite being told
  not to? If so, that's a genuinely useful thing to report honestly — it
  shows you understand the tool's limits, which is exactly what "AI
  native" should mean: knowing where to trust it and where not to.
