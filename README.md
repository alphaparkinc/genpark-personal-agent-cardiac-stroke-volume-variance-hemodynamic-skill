# Cardiac Stroke Volume Variance (SVV) & Preload Responsiveness Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `assess_stroke_volume_variance`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates Stroke Volume Variation (SVV) and Pulse Pressure Variation (PPV) across mechanical/spontaneous respiratory cycles, predicting left ventricular fluid responsiveness and hemodynamic stability.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Hemodynamics)`

## MCP Tool Specification
### `assess_stroke_volume_variance`
Parameters:
- `sv_series` (list): Time series of stroke volume measurements (in mL) across respiratory cycles
- `systolic_bp_series` (list): Systolic arterial blood pressure readings (mmHg)
- `diastolic_bp_series` (list): Diastolic arterial blood pressure readings (mmHg)
- `mean_arterial_pressure` (float): Mean arterial pressure (MAP, mmHg)
- `heart_rate_bpm` (float): Resting heart rate in beats per minute

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-cardiac-stroke-volume-variance-hemodynamic-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-cardiac-stroke-volume-variance-hemodynamic-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
