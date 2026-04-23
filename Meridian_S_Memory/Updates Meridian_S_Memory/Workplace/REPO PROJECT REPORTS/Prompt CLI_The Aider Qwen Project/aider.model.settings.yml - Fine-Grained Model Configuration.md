---
modified: 2026-04-19T04:35:50+03:00
---
# ============================================================
# .aider.model.settings.yml - Fine-Grained Model Configuration
# Location: Same directory as .aider.conf.yml
# ============================================================

# ------------------------------------------------------------
# Qwen3-Coder-Plus - ARCHITECT MODEL
# ------------------------------------------------------------
- name: openai/qwen3-coder-plus
  edit_format: whole
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  # Qwen3-Coder-Plus supports 128k context
  extra_params:
    max_tokens: 8192
  # For reasoning models like QwQ, you might enable include_reasoning: true
  # But Qwen3-Coder-Plus doesn't require it by default
  caches_by_default: true
  # Editor model association (for architect mode)
  editor_model_name: openai/qwen3-coder-turbo
  editor_edit_format: editor-diff

# ------------------------------------------------------------
# Qwen3-Coder-Turbo - EDITOR MODEL
# ------------------------------------------------------------
- name: openai/qwen3-coder-turbo
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 4096
  caches_by_default: true
  # Weak model association
  weak_model_name: openai/qwen3.5-plus
  editor_edit_format: editor-diff

# ------------------------------------------------------------
# Qwen3.5-Plus - WEAK MODEL (Fallback/Utility)
# ------------------------------------------------------------
- name: openai/qwen3.5-plus
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 4096
  caches_by_default: true
  # Can also be used as editor for simpler tasks
  editor_edit_format: editor-diff