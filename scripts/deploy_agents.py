#!/usr/bin/env python3
"""
Master Deployment Script for the Autonomous AI Ecosystem

This script launches all major components concurrently:
  - Core Execution Engine
  - Microkernel AI
  - AI Agent Manager
  - Orchestrator (with OpenLLaMA 7B)
  - Event Bus
  - Dashboard Server

Ensure the virtual environment is activated before running.
"""
import subprocess, time, logging
from pathlib import Path
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  filename=str(Path(__file__).parent.parent / "logs/deployment.log"),
  filemode="a"
)
def deploy_agents():
    base_dir = Path(__file__).parent.parent.resolve()
    subprocess.Popen(["python3", str(base_dir / "core/execution_engine.py")])
    subprocess.Popen(["python3", str(base_dir / "microkernel/microkernel_ai.py")])
    subprocess.Popen(["python3", str(base_dir / "agents/ai_agent_manager.py")])
    subprocess.Popen(["python3", str(base_dir / "microkernel/orchestrator.py")])
    subprocess.Popen(["python3", str(base_dir / "communication/event_bus.py")])
    subprocess.Popen(["python3", str(base_dir / "dashboard/dashboard.py")])
    print("Deployment completed successfully.")
    time.sleep(5)
if __name__ == "__main__":
    deploy_agents()
