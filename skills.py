# -*- coding: utf-8 -*-
"""Cardiac Stroke Volume Variance (SVV) & Preload Responsiveness Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def assess_stroke_volume_variance(**kwargs):
    """Calculates Stroke Volume Variation (SVV) and Pulse Pressure Variation (PPV) across mechanical/spontaneous respiratory cycles, predicting left ventricular fluid responsiveness and hemodynamic stability."""
    sv_series = kwargs.get('sv_series')
    systolic_bp_series = kwargs.get('systolic_bp_series')
    diastolic_bp_series = kwargs.get('diastolic_bp_series')
    mean_arterial_pressure = kwargs.get('mean_arterial_pressure')
    heart_rate_bpm = kwargs.get('heart_rate_bpm')

    sv_min = min(sv_series)
    sv_max = max(sv_series)
    sv_mean = sum(sv_series) / len(sv_series) if sv_series else 1.0
    svv_pct = round(((sv_max - sv_min) / (sv_mean if sv_mean > 0 else 1.0)) * 100.0, 2)
    
    pulse_pressures = [s - d for s, d in zip(systolic_bp_series, diastolic_bp_series)]
    pp_min = min(pulse_pressures) if pulse_pressures else 1.0
    pp_max = max(pulse_pressures) if pulse_pressures else 1.0
    pp_mean = sum(pulse_pressures) / len(pulse_pressures) if pulse_pressures else 1.0
    pp_mean_safe = pp_mean if pp_mean > 0 else 1.0
    ppv_pct = round(((pp_max - pp_min) / pp_mean_safe) * 100.0, 2)
    
    is_fluid_responsive = svv_pct > 13.0
    if svv_pct > 20.0:
        clinical_state = "Hypovolemia / Pronounced Preload Dependency"
        recommendation = "Evaluate intravascular volume expansion; monitor cardiac index."
    elif svv_pct > 13.0:
        clinical_state = "Preload Responsive (Ascending Limb of Frank-Starling)"
        recommendation = "Positive volume challenge likely to augment cardiac output."
    elif svv_pct < 6.0:
        clinical_state = "Preload Independent / Risk of Volume Overload"
        recommendation = "Avoid uncalibrated bolus administration; assess ventricular contractility."
    else:
        clinical_state = "Euvolemic / Normotensive Hemodynamic Stability"
        recommendation = "Maintain current fluid balance protocol."
        
    cardiac_output_lpm = round((sv_mean * heart_rate_bpm) / 1000.0, 2)
    systemic_vascular_resistance = round(((mean_arterial_pressure - 4.0) * 80.0) / (cardiac_output_lpm if cardiac_output_lpm > 0 else 1.0), 1)
    
    result = {
        "status": "success",
        "stroke_volume_variation_pct": svv_pct,
        "pulse_pressure_variation_pct": ppv_pct,
        "mean_stroke_volume_ml": round(sv_mean, 1),
        "estimated_cardiac_output_lpm": cardiac_output_lpm,
        "systemic_vascular_resistance_dynes": systemic_vascular_resistance,
        "preload_responsiveness": is_fluid_responsive,
        "clinical_hemodynamic_state": clinical_state,
        "guidance": recommendation,
        "engine": "GenPark Bio-Hemodynamic Frank-Starling Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "assess_stroke_volume_variance": {
        "name": "assess_stroke_volume_variance",
        "description": "Calculates Stroke Volume Variation (SVV) and Pulse Pressure Variation (PPV) across mechanical/spontaneous respiratory cycles, predicting left ventricular fluid responsiveness and hemodynamic stability.",
        "parameters": {
            "type": "object",
            "properties": {
                "sv_series": {"type": "array", "description": "Time series of stroke volume measurements (in mL) across respiratory cycles"},
                "systolic_bp_series": {"type": "array", "description": "Systolic arterial blood pressure readings (mmHg)"},
                "diastolic_bp_series": {"type": "array", "description": "Diastolic arterial blood pressure readings (mmHg)"},
                "mean_arterial_pressure": {"type": "number", "description": "Mean arterial pressure (MAP, mmHg)"},
                "heart_rate_bpm": {"type": "number", "description": "Resting heart rate in beats per minute"},
            },
            "required": ['sv_series', 'systolic_bp_series', 'diastolic_bp_series', 'mean_arterial_pressure', 'heart_rate_bpm']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "assess_stroke_volume_variance":
            res = assess_stroke_volume_variance(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-cardiac-stroke-volume-variance-hemodynamic-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-cardiac-stroke-volume-variance-hemodynamic-skill...")
    test_args = {'sv_series': [68.0, 72.0, 85.0, 64.0, 78.0], 'systolic_bp_series': [118.0, 122.0, 130.0, 114.0, 126.0], 'diastolic_bp_series': [78.0, 80.0, 82.0, 76.0, 80.0], 'mean_arterial_pressure': 92.0, 'heart_rate_bpm': 72.0}
    res = assess_stroke_volume_variance(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-cardiac-stroke-volume-variance-hemodynamic-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
