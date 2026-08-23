# GST E-Invoice Compliance Rules (Reference Ruleset)

This is a simplified rule set covering the most common mandatory fields and
checks for a valid B2B GST e-invoice in India. It is used as grounding
context for the compliance checker — the model is instructed to check every
invoice against these rules only, not against general knowledge, so its
findings stay traceable to a specific rule.

## Mandatory Fields
1. **Seller GSTIN** — must be a valid 15-character GSTIN.
2. **Buyer GSTIN** — must be a valid 15-character GSTIN for B2B invoices.
3. **Invoice Reference Number (IRN)** — mandatory for B2B invoices above the
   e-invoicing turnover threshold. Must not be blank.
4. **QR Code** — must be present (`qr_code_present: true`) whenever an IRN is
   required.
5. **HSN Code** — every line item must carry a valid HSN code. Must not be
   blank.
6. **Place of Supply** — must be present and must be a valid Indian state.

## Tax Calculation Rules
7. **Intrastate sales** (seller and place of supply in the same state) must
   split tax as CGST + SGST, each at half the applicable GST rate. IGST must
   be 0.
8. **Interstate sales** (seller and place of supply in different states)
   must charge IGST only, at the full applicable GST rate. CGST and SGST
   must both be 0.
9. **Arithmetic check** — `taxable_value + cgst + sgst + igst` must equal
   `total_value` for the invoice (summed across line items). Flag any
   mismatch, however small.
10. **GST rate sanity check** — common electronics/office-equipment HSN
    codes are typically taxed at 18%. A materially different rate (e.g. 12%,
    5%) on a similar product should be flagged as a possible
    misclassification, not treated as a hard error — call this out as a
    "possible issue" rather than a certain one.

## Output Expectations
For each invoice, identify:
- Whether it is fully compliant
- Each specific rule violated (by rule number and short description)
- A one-line suggested fix per issue
- A severity: `blocking` (invoice cannot be filed as-is) vs. `warning`
  (worth reviewing, not necessarily wrong)

Do not invent rules beyond this list. If something looks unusual but isn't
covered by a rule above, note it as an observation, not a violation.
