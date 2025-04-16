#!/usr/bin/env python3
"""
Orchestrator Module with Local LLM Integration

Uses OpenLLaMA 7B to generate recommendations based on configuration.
Logs to ${PROJECT_BASE_DIR}/logs/orchestrator.log.
"""
import time, json, logging
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL_NAME = "openlm-research/open_llama_7b"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  filename=str(Path(__file__).parent.parent / "logs/orchestrator.log"),
  filemode="a"
)
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, legacy=False)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.to(device)
    logging.info("Local LLM loaded successfully.")
except Exception as e:
    logging.error(f"LLM load error: {e}")
    raise
def load_parameters():
    with open(Path(__file__).parent.parent / "config/system_parameters.json") as f:
        return json.load(f)
def generate_recommendation(prompt):
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.5)
        rec = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logging.info("Recommendation generated.")
        return rec
    except Exception as e:
        logging.error(f"Generation error: {e}")
        return "LLM generation error."
def orchestrate():
    params = load_parameters()
    prompt = f"Current parameters: {json.dumps(params)}. Recommend optimizations for scheduling, resources, and error handling."
    logging.info(f"Orchestrator prompt: {prompt}")
    rec = generate_recommendation(prompt)
    if rec:
        logging.info(f"LLM Recommendation: {rec}")
        print(f"LLM Recommendation:\n{rec}\n")
    else:
        logging.error("No recommendation received.")
if __name__ == "__main__":
    while True:
        orchestrate()
        time.sleep(30)
