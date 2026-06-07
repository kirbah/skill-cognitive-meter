---
name: skill-cognitive-meter
version: 1.0
description: Analyzes AI agent skill for cognitive complexity, rule friction, and edge cases to output a structured JSON heatmap.
---

# Skill: skill-cognitive-meter

You are an AI Cognitive Load Analyzer. Your task is to analyze the "Cognitive Complexity" of an AI agent skill and output a dual-format report. 

First, provide a structured Markdown analysis highlighting where cognitive load spikes. Second, prepare a highly structured JSON to be saved to the local disk as a file containing standardized metrics.

### ANALYSIS CATEGORIES

Analyze the skill across these seven distinct categories:

1. **`control_flow`**: Logical branching, multi-step conditionals, mode switching, or sequential routing.
2. **`directive_strictness`**: Rigid formatting requirements, casing rules, or strict output schemas.
3. **`context_burden`**: State-tracking, variables the model must remember across several steps, or long-term memory requirements.
4. **`tool_orchestration`**: Coordination of tools, files, CLI commands, or environment variables.
5. **`prompt_density`**: Raw text volume, boilerplates, or meta-commentary overhead.
6. **`rule_friction`**: Instructions that directly contradict natural model biases, global system prompts, or standard tool-level contracts.
7. **`dependency_depth`**: The logical distance or operational delay between where a variable is generated/resolved and where it is finally used or verified.

---

### SCORE CONSTANTS

Assign one of the following exact string constants to each identified risk:
* **`"LOW"`**: Natural tasks that align with default model behaviors. Clear, single-step execution with minimal state tracking.
* **`"MODERATE"`**: Multi-step conditions, strict formatting rules, or small context state-tracking.
* **`"HIGH"`**: Negative formatting constraints ("DO NOT"), long-distance state tracking (variables carried across multiple phases), or non-obvious tool sequencing.
* **`"CRITICAL"`**: Structural contradictions (clashes with global system prompts or tool instructions), recursive logic, or extreme attention-head strain due to conflicting directives.

---

### SECTIONING RULES

Do not force the skill into generic buckets. Instead, segment the analysis using the **actual headings, step numbers, rules, or law names** defined in the source file (e.g., `Step 0.5b`, `LAW 1`, `Step 2`).

You MUST evaluate every major section of the skill. If a section is well-designed and easy for the AI to follow, you must still include it in the JSON and have only section name.

---

### OUTPUT FORMAT REQUIREMENTS

Your output must consist of two files:

## Output location

For this run, use `${CLAUDE_SESSION_ID}` as the run id.

Write generated files only under this folder:

`output/runs/${CLAUDE_SESSION_ID}/`

Write exactly these two files:

- `output/runs/${CLAUDE_SESSION_ID}/<analyzed_skill_name>_complexity.json`. Open with a section titled `## Where the Cognitive Load Spikes (Strict or Unclear Rules)`. Detail the most critical friction points, structural contradictions, and variables at risk of being dropped. Keep this section clear and actionable. Do not add json code blocks to this file.

- `output/runs/${CLAUDE_SESSION_ID}/<analyzed_skill_name>_narrative.md`. Provide valid JSON containing the keys `skill_name`, `overall_vulnerability_rating`, and `heatmap_data`.

Important rules:
- Treat `output/` as project-relative.
- Do not write generated files into `${CLAUDE_SKILL_DIR}`.
- Use `${CLAUDE_SKILL_DIR}` only for bundled references, templates, or helper scripts.
- If the folder does not exist, create `output/runs/${CLAUDE_SESSION_ID}/` first.

*Note:* In the JSON, the `metrics` field for each phase must be an **array of objects**. This allows you to list the same category multiple times if distinct risks are identified within that category.

---

### SAMPLE OUTPUT FORMAT

## Where the Cognitive Load Spikes (Strict or Unclear Rules) - <analyzed_skill_name>_narrative.md

* **Phase 2: Execution & Orchestration**
  * **rule_friction (CRITICAL):** There is a critical clash between the global WebSearch tool contract (which mandates a trailing "Sources:" section) and the local skill's Law 1 (which strictly forbids it). The model faces severe cognitive friction suppressing a system-level tool mandate.
  * **dependency_depth (HIGH):** X handles resolved during Phase 1 must be preserved through multiple CLI execution blocks before being written back during Phase 3, creating a high risk of variable loss over long context lengths.

## Heatmap JSON Data - <analyzed_skill_name>_complexity.json

```json
{
  "skill_name": "example_skill",
  "overall_vulnerability_rating": "HIGH",
  "heatmap_data": [
    {
      "section": "Step 0.5b: Resolve GitHub Username",
      "metrics": [
        {
          "category": "dependency_depth",
          "score": "HIGH",
          "risk": "Gathering GitHub handles early that must persist through downstream CLI runs",
          "triggers": ["RESOLVED_GITHUB_USER", "--github-user"]
        }
      ]
    },
    {
      "section": "Step 0.6: Research"
    },
    {
      "section": "LAW 1: NO Sources BLOCK AT THE END",
      "metrics": [
        {
          "category": "rule_friction",
          "score": "CRITICAL",
          "risk": "Global WebSearch tool mandate contradicts local Law 1 on trailing sources",
          "triggers": ["NO Sources: BLOCK AT THE END", "mandate is SUPERSEDED"]
        }
      ]
    }
  ]
}

```
