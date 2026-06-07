# 🧠 skill-cognitive-meter

[![GitHub stars](https://img.shields.io/github/stars/kirbah/skill-cognitive-meter?style=social)](https://github.com/kirbah/skill-cognitive-meter/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Visualize, measure, and optimize the cognitive load of your **Claude Code** and AI Agent skills before they degrade execution reliability.

[**Explore the Live Sample Report**](https://kirbah.github.io/skill-cognitive-meter/)

---

## The Problem: The Prompt Patching Anti-Pattern

When an AI agent fails an edge case, the intuitive developer reaction is to patch the prompt by adding more instructions, rigid rules, or negative constraints ("DO NOT..."). Over time, this creates cumulative **cognitive load**:

* **Rule Friction**: Direct contradictions between local rules and global tool contracts.
* **Dependency Depth**: Requiring the model to carry variables over long context spans.
* **Attention Strain**: Overwhelming the model's processing window, which directly correlates with increased hallucinations and looping.

Instead of guessing where your instructions are failing, `skill-cognitive-meter` analyzes your Claude skill definition and maps out complexity hotspots dynamically.

---

## Interactive Heatmap

[![Cognitive Heatmap Screenshot](https://raw.githubusercontent.com/kirbah/skill-cognitive-meter/main/docs/images/skill-cognitive-meter-demo.webp)](https://kirbah.github.io/skill-cognitive-meter/)
*Click the image to view the live interactive dashboard.*

---

## Key Metrics Evaluated

The tool grades your skill layout across seven standard cognitive dimensions:

1. **Rule Friction**: Clashes with system-level tool constraints or natural biases.
2. **Dependency Depth**: The distance between where a state variable is generated and where it is verified.
3. **Control Flow**: Logical branching, mode-switching, and decision-tree density.
4. **Context Burden**: State-tracking volume across sequential phases.
5. **Tool Orchestration**: CLI, tool calls, and environment configuration complexity.
6. **Prompt Density**: Raw text volume and boilerplates.
7. **Directive Strictness**: Schema rigidness, casing constraints, and negative styling rules.

---

## How to Use It

### 1. Setup
Copy the `skill-cognitive-meter` directory into your local skills folder (e.g., where you keep your `.claude` or agent configurations).

### 2. Execute the Analyzer in Claude
Ask Claude to load the skill and run it against the target skill file you want to evaluate. 

**Example Prompt:**
> "Use the cognitive-meter skill to analyze my custom web-search skill located at `skills/web-search/SKILL.md`."

The system generates two artifact files in your output directory:
* `output/runs/<run_id>/<skill_name>_complexity.md` (Detailed written narrative)
* `output/runs/<run_id>/<skill_name>_narrative.json` (Structured metric points)

### 3. Build the Visual Report
Use the built-in Python builder to merge your analysis runs into the interactive HTML template:
```bash
python skills/skill-cognitive-meter/scripts/build_report.py
```

### 4. Review Results
Open `pages/index.html` (or your local build output) in any browser to interactively explore the complexity spikes across your files. Use this data to refactor overloaded instructions and improve your agent's reliability.

---

## Directory Structure

```text
└── kirbah-skill-cognitive-meter/
    ├── pages/                      # Static host directory for GitHub Pages
    │   └── index.html              # Interactive dashboard UI
    ├── skills/
    │   └── skill-cognitive-meter/
    │       ├── SKILL.md            # Skill for cognitive load analysis
    │       ├── assets/
    │       │   └── report-template.html
    │       └── scripts/
    │           └── build_report.py # Generates the integrated visual report
    └── .claude/                    # Platform alignment configurations
```