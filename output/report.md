# Billeasy GST E-Invoice Compliance Report

**Summary:** 2/8 invoices fully compliant.

## BE-INV-1001 — ❌ Issues found

- **[BLOCKING] 7 Intrastate sales tax split incorrect** — For intrastate sale, CGST and SGST should each be half of the GST rate; IGST should be 0. The invoice uses IGST 900 and no CGST/SGST.
  - Fix: Split the tax into CGST=450 and SGST=450 (18% of 5000 ÷ 2) and set IGST to 0.

## BE-INV-1002 — ❌ Issues found

- **[BLOCKING] 3: IRN required** — IRN is missing for B2B invoice above threshold
  - Fix: Generate and include a valid IRN.
- **[BLOCKING] 4: QR Code required** — QR code is missing while IRN is required
  - Fix: Generate the QR code and include it with the invoice.

## BE-INV-1003 — ❌ Issues found

- **[BLOCKING] 5. Mandatory HSN Code** — HSN code missing on line item
  - Fix: Provide a valid HSN code for each line item.
- **[BLOCKING] 7. Intrastate Tax Split** — Incorrect tax distribution: IGST used instead of CGST and SGST for intrastate sale
  - Fix: Split tax into CGST and SGST, each 50% of GST amount; set IGST to 0.

## BE-INV-1004 — ❌ Issues found

- **[BLOCKING] Rule 7 - Intrastate tax split** — CGST and SGST amounts do not match half of the applicable 18% GST rate on taxable value.
  - Fix: Recalculate CGST and SGST as 9% each of taxable value (i.e., ₹1620 each).
- **[BLOCKING] Rule 9 - Arithmetic mismatch** — Sum of taxable value, CGST, SGST, IGST (21600) does not equal total_value (21599).
  - Fix: Adjust total_value to ₹21240 (18000 + 1620 + 1620).

## BE-INV-1005 — ❌ Issues found

- **[BLOCKING] 2. Buyer GSTIN** — Buyer GSTIN is not a valid 15-character GSTIN.
  - Fix: Provide a correct 15-character GSTIN for the buyer.
- **[BLOCKING] 7. Intrastate Tax Split** — For intrastate sale, CGST and SGST should each be half of the tax amount and IGST must be 0, but the invoice uses IGST only.
  - Fix: Adjust tax calculation: set CGST and SGST each to 1080 and set IGST to 0.

## BE-INV-1006 — ✅ Compliant

No issues found.


## BE-INV-1007 — ❌ Issues found

- **[BLOCKING] 7 - Intrastate tax split** — For intrastate sale, CGST and SGST should be applied and IGST must be zero. Current invoice shows CGST=0, SGST=0, IGST=3600.
  - Fix: Apply CGST=1800 and SGST=1800 (each half of 12% on 20000) and set IGST=0.
- **[WARNING] 10 - GST rate sanity check** — HSN 851762 typically taxed at 18%. Invoice uses 12%.
  - Fix: Verify HSN mapping; if correct, consider changing GST rate to 18% or justify 12% rate.

## BE-INV-1008 — ✅ Compliant

No issues found.

