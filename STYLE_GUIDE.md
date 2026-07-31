# FIXReader Editorial Style Guide

This document defines preferred terminology, formatting, and writing conventions for all FIXReader documentation. Follow it when adding or editing any user-facing content.

---

## FIX Terminology

### Message Names

Use the official FIX specification names. Two-word message names are written as two words in prose.

| Correct | Avoid |
|---|---|
| Resend Request (35=2) | ResendRequest |
| Sequence Reset (35=4) | SequenceReset |
| Test Request (35=1) | TestRequest |
| Execution Report (35=8) | ExecutionReport |
| New Order Single (35=D) | NewOrderSingle |
| Allocation Instruction (35=J) | AllocationInstruction |
| Allocation Instruction Ack (35=P) | AllocAck |
| Don't Know Trade (35=Q) | DKTrade |

**Exception:** When referencing message names in code blocks, log output, or engine configuration files, use the implementation-specific form (e.g., `ResendRequest` in QuickFIX engine logs).

### Session Concepts

| Correct | Avoid |
|---|---|
| Gap Fill | GapFill |
| session layer | session-layer |
| application layer | app layer |

### Field Names

When referencing a FIX tag in descriptive text, use the format: **FieldName (N)** where N is the tag number.

| Correct | Avoid |
|---|---|
| PossDupFlag (43) = Y | PossDupFlag=Y, Tag 43=Y |
| GapFillFlag (123) = Y | GapFillFlag=Y |
| MsgSeqNum (34) | Tag 34 |
| SenderCompID (49) | SenderCompID |
| ResetSeqNumFlag (141) | ResetSeqNumFlag=Y (no tag) |
| ExecID (17) | Tag 17 |
| CumQty (14) | cumqty |

When the tag number is not known, use the field name alone: `SenderCompID`, `TargetCompID`.

### ExecType Values

ExecType (150) changed between FIX versions. Always specify the version when describing values:

| Value | FIX 4.2 | FIX 4.4 / 5.0 |
|---|---|---|
| `1` | Partial Fill | (deprecated) |
| `2` | Fill | (deprecated) |
| `F` | — | Trade/fill |

When the page covers both versions, present both forms explicitly.

### Enumeration Values

Use **Enumeration Values** (not "Enum Values" or "enum values") when labeling appendix sections or describing the set of valid values for a field.

---

## Spelling and Grammar

### American English

FIXReader targets US financial practitioners. Use American spelling throughout.

| Correct | Avoid |
|---|---|
| acknowledgment | acknowledgement |
| acknowledgments | acknowledgements |
| canceled | cancelled |
| synchronized | synchronised |

### Punctuation in Headings

Do not use `&` in section headings. Write "and" in full.

| Correct | Avoid |
|---|---|
| Heartbeat and TestRequest Diagnostics | Heartbeat & TestRequest Diagnostics |
| Firewall and Port Configuration | Firewall & Port Configuration |
| SSL/TLS Configuration | SSL / TLS Configuration |

Note: `SSL/TLS` uses a slash with no spaces.

### Sentence Fragments

Section headings may be noun phrases (no verb required). Body text must be complete sentences.

**Avoid sentence fragments in 5-Minute Diagnosis summaries.** Each item must be a complete sentence or complete question.

---

## Technical Accuracy

### Do Not Invent FIX Behavior

All tag numbers, message types, and field descriptions must be sourced from `fixreader_data/fix_tags.json` or the official FIX Trading Community specifications.

- Do not use placeholder tag values in examples. Use real or clearly-labeled placeholder values.
- Checksum (`10=`) examples must use `10=000` as a placeholder, not `10=xxx` or `10=NNN`.
- Do not describe deprecated fields without noting the deprecation and affected versions.

### Deprecated Fields

When a field is deprecated in a later FIX version, note it at the point of reference:

> ExecBroker (76) — valid in FIX 4.2; deprecated in FIX 4.4+.

### ResetOnLogon vs ResetSeqNumFlag

These are different things:

- **ResetOnLogon** — a FIX engine configuration key (engine-level setting). Not a FIX protocol tag.
- **ResetSeqNumFlag (141)** — a FIX protocol field sent in the Logon message (35=A).

Do not conflate them. When describing both, keep them as separate concepts.

---

## Test Count Accuracy (Cert Pages)

Subtitle test counts must match the `ROWS` array length exactly. Count rows before publishing:

```
s1 rows + s2 rows + ... + sN rows = subtitle count
```

---

## Cross-Links

### When to Link

Link when the target page directly elaborates on the concept being described. Examples:

- Reference to fill reconciliation on a page about duplicate orders → link to `/troubleshooting/fill-reconciliation`
- Reference to gap fill in a sequence numbers article → link to `/troubleshooting/gap-fill`
- Reference to a FIX tag number in troubleshooting → link to `/tag/{N}`

### When Not to Link

- Do not add links that repeat information already on the same page.
- Do not link every occurrence of a term — link once per section at most.
- Do not link to external resources from the main content body unless the resource is canonical (e.g., FIX Trading Community spec).

---

## Code Examples

- Use `|` as the field delimiter in FIX message examples.
- Omit the checksum or use `10=000` as a placeholder.
- Always label the message type (`35=X`) so the reader can identify the message.
- Keep examples minimal — show only the fields relevant to the point being made.
- Use `OUT` and `IN` prefixes when showing a request-response exchange.

**Example:**
```
OUT 35=A|49=CLIENTA|56=EXCHANGE|34=1|98=0|108=30|
IN  35=5|58=Invalid SenderCompID|
```

---

## Section Structure (Troubleshooting Pages)

Each troubleshooting article should follow this order where applicable:

1. **Critical Warning** — the most important thing not to do
2. **Quick Triage** — 5–8 ordered diagnostic steps
3. **Common Problems** — symptom/cause/check table
4. **Key Fields** — relevant FIX tags with descriptions
5. **Reading the Logs** — annotated FIX message examples
6. **Recovery Checklist** — ordered steps with checkboxes
7. **5-Minute Diagnosis** — concise summary (TL;DR)

Not all sections are required for every article. Include only what adds value.
