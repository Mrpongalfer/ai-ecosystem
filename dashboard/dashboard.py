#!/usr/bin/env python3
"""
Dashboard Server for the Autonomous AI Ecosystem

Provides REST API endpoints to view/update system configuration, retrieve logs, and trigger reconfiguration.
Also serves a web dashboard at the root URL.
"""
from flask import Flask, jsonify, request, render_template
import json
from pathlib import Path
app = Flask(__name__)
CONFIG_PATH = Path(__file__).parent.parent / "config/system_parameters.json"
LOGS_DIR = Path(__file__).parent.parent / "logs"
def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)
def update_config(new_config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(new_config, f, indent=4)
    return True
def read_log(log_filename, lines=50):
    log_file = LOGS_DIR / log_filename
    if log_file.exists():
        with open(log_file) as f:
            return f.readlines()[-lines:]
    else:
        return ["Log file does not exist."]
@app.route("/")
def index():
    config = load_config()
    exec_log = read_log("execution_engine.log")
    micro_log = read_log("microkernel_ai.log")
    orchestrator_log = read_log("orchestrator.log")
    agent_log = read_log("ai_agent_manager.log")
    return render_template("index.html", config=config,
                           exec_log=exec_log,
                           micro_log=micro_log,
                           orchestrator_log=orchestrator_log,
                           agent_log=agent_log)
@app.route("/api/config", methods=["GET"])
def api_get_config():
    return jsonify(load_config())
@app.route("/api/config", methods=["POST"])
def api_update_config():
    new_config = request.json
    return (jsonify({"status": "Configuration updated."}) if update_config(new_config)
            else jsonify({"status": "Update failed."}), 500)
@app.route("/api/log/<log_name>", methods=["GET"])
def api_get_log(log_name):
    return jsonify(read_log(log_name))
@app.route("/api/reconfigure", methods=["POST"])
def api_reconfigure():
    config = load_config()
    return jsonify({"status": "Reconfiguration triggered", "config": config})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
