# Executor Integration Notes
*How the wrapper plugs into the MeridianSignal pipeline.*

## Install
```
pipx install aider-chat
export AIDER_MODEL=deepseek/deepseek-chat   # or any LiteLLM-routable model
export DEEPSEEK_API_KEY=...                 # or provider of choice
```

## Run
```
python executor.py --plan ./plan.md --design ./design.md --task P1-T1
python executor.py --plan ./plan.md --design ./design.md --phase P1
python executor.py --plan ./plan.md --design ./design.md --auto
```

## Guarantees
- Each task is one Aider `--message` invocation; no interactive loop.
- No auto-commits. Wrapper commits only when the parsed Task Report status == COMPLETE.
- Reports are persisted to `./reports/<task_id>.md` and are the single source of truth
  for dependency resolution on subsequent runs.
- Dependencies are enforced against those reports, not against git log.
- On DEVIATED / BLOCKED / ESCALATION the wrapper stops and exits non-zero.

## Next steps (map to ActiveWork.md priorities)
1. Drop `design_md_format_spec.md` content into `Projects/MeridianPipeline.md` as
   the Section "design.md Format Spec v1.0".
2. Update `Agents/designer_agent.md` Section "Output: design.md" to emit the
   fenced YAML blocks (`component`, `entity`, `interface`, `behavior`, `open_question`)
   and the three header comments.
3. Add `executor.py` to a new `scripts/` folder and wire it into the Executor
   stage. Add a thin `validate_design.py` that enforces Section 5 of the spec.
4. Run one end-to-end smoke test on a trivial idea (e.g. "a CLI that counts
   words in a markdown file") to validate the Brainstormer → Executor chain.
5. Collect that first run's artifacts as training data for DSPy Phase 5 unblock.