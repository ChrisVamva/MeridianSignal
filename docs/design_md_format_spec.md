# design.md Format Specification v1.0
*The contract between Designer (Stage 6) and Planner (Stage 7).*
*Binding for all pipeline runs. Parseable by deterministic regex.*

---

## 1. Purpose

The Designer agent currently produces freeform markdown. The Planner cannot reliably
extract Architecture components, Behavior specs, or Open Questions without a fixed
contract. This spec locks that contract.

Every design.md produced by the Designer MUST conform. The Planner MAY refuse to
process any design.md that fails the validator in Section 5.

---

## 2. File Layout (Exact Order, Exact Headings)

```
# design.md — <PRODUCT NAME>
<!-- schema: meridian-design/1.0 -->
<!-- source_brief: <research_brief_id_or_date> -->
<!-- generated: <ISO-8601 UTC> -->

## 1. System Overview
## 2. User Model
## 3. Architecture
## 4. Core Data Model
## 5. Interface Specification
## 6. Behavior Specification
## 7. Constraints and Non-Negotiables
## 8. Open Questions
```

Rules:
- Top-level H1 MUST match `^# design\.md — .+$`.
- The three HTML comments MUST appear in order directly under the H1.
- Section headings MUST be H2 and MUST appear in the exact order above.
- No additional H2 sections are permitted.
- Sub-structure within each section uses H3/H4 only.

---

## 3. Required Block Schemas (Per Section)

### 3.1 System Overview
```
### Does
<2–3 sentences, no bullets>

### Does NOT
- <scope boundary bullet>
- <scope boundary bullet>

### Design Principles
- <principle 1>
- <principle 2>
```
- 1–3 principles, no more.

### 3.2 User Model
```
### Primary User
- Role: <text>
- Technical level: <Novice | Intermediate | Advanced>
- Context of use: <text>

### Secondary Users
- <bullet or "None">

### Goals
- <goal>

### Constraints
- <constraint>
```

### 3.3 Architecture
Each component is emitted as a fenced YAML block tagged `component`.
Planner parses these with `grep -A 100 '^```component$'` style extraction.

```
```component
id: C1
name: <ComponentName>
responsibility: <one sentence>
inputs: [<input1>, <input2>]
outputs: [<output1>]
depends_on: [<C-id>, ...]
risk: Low | Med | High
```
```

Additional required subsections:
```
### Data Flow
<ASCII or text arrows, one line per major path>
input → <Cx> → <Cy> → output

### External Dependencies
| Name | Purpose | Risk |
|------|---------|------|
| <pkg/service> | <why> | Low/Med/High |
```

### 3.4 Core Data Model
Each entity as a fenced YAML block tagged `entity`.
```
```entity
name: <EntityName>
persistence: persisted | ephemeral
fields:
  - name: <field>
    type: string | int | bool | datetime | uuid | json | ref:<Entity>
    required: true | false
relationships:
  - <EntityA> 1..N <EntityB>
```
```

### 3.5 Interface Specification
Each interface as a fenced YAML block tagged `interface`.
```
```interface
id: I1
kind: UI | API | CLI | FileFormat
name: <name>
inputs:
  - <name>: <type/description>
outputs:
  - <name>: <type/description>
states: [<state1>, <state2>]
errors:
  - code: <slug>
    when: <trigger>
    response: <observable behavior>
```
```

### 3.6 Behavior Specification
Each behavior as a fenced YAML block tagged `behavior`.
```
```behavior
id: B1
trigger: <user action or event>
process: <ordered steps, 1 line each, separated by " → ">
outcome: <observable result>
edge_cases:
  - when: <condition>
    then: <behavior>
failure_states:
  - when: <failure>
    then: <behavior>
```
```

### 3.7 Constraints and Non-Negotiables
```
| ID | Category | Constraint | Immutable Post-Launch |
|----|----------|------------|-----------------------|
| CN1 | cost | $0/month infra | Yes |
| CN2 | runtime | must run on <env> | Yes |
| CN3 | privacy | <requirement> | Yes |
```
Categories: `cost | runtime | privacy | security | performance | legal`.

### 3.8 Open Questions
Each question as a fenced YAML block tagged `open_question`.
```
```open_question
id: OQ1
question: <one sentence>
why_it_matters: <one sentence>
assumption_made: <text or "None">
blocks: [<section-or-component-id>]
```
```
All `[ASSUMPTION: ...]` flags from earlier sections MUST also appear as OQ entries.

---

## 4. Parsing Contract (Planner-Facing)

The Planner extracts by regex against the fenced blocks:

| Source | Regex | Binds To |
|--------|-------|----------|
| component | ```^```component\n(.*?)\n```$``` | Task owner groups per component |
| entity | ```^```entity\n(.*?)\n```$``` | Data-layer tasks |
| interface | ```^```interface\n(.*?)\n```$``` | Interface implementation tasks |
| behavior | ```^```behavior\n(.*?)\n```$``` | Behavior-level acceptance tests |
| open_question | ```^```open_question\n(.*?)\n```$``` | plan.md Section 6, tagged `[FROM DESIGN]` |

IDs are stable across the pipeline:
- Components `Cn`, Entities unique by `name`, Interfaces `In`, Behaviors `Bn`,
  Constraints `CNn`, Open Questions `OQn`.
- Planner Task IDs reference these: e.g. task `P2-T4` may list `implements: [C3, B2]`.

---

## 5. Validator (Ship-Blocking)

Before handing design.md to the Planner, run the validator. Failure = regenerate.

Check list:
- [ ] H1 matches pattern.
- [ ] Three schema/source/generated comments present.
- [ ] All 8 H2 sections present, in order, no extras.
- [ ] At least one `component`, one `entity`, one `interface`, one `behavior` block.
- [ ] Every component has id, name, responsibility, risk.
- [ ] Every open_question has id and `blocks:` list (may be empty `[]`).
- [ ] Every `[ASSUMPTION:...]` inline flag has a matching OQ entry.
- [ ] No prose inside fenced YAML blocks.
- [ ] No planning language anywhere (no "phase", "sprint", "week N", "we will").

Reference implementation: `scripts/validate_design.py` (to be added in
Executor milestone M1).

---

## 6. Versioning

This spec is `meridian-design/1.0`. Breaking changes bump the major. The
schema comment at the top of every design.md MUST match the version the
Planner expects, or the Planner refuses to parse.

---

## 7. Migration Note

Existing Designer prompt (`Agents/designer_agent.md`) must be updated so
its output rules mirror Sections 2–3 of this spec exactly. Add a final
"Emit schema comment `<!-- schema: meridian-design/1.0 -->`" instruction.
