#!/bin/bash
# Elite-Tier Configuration Settings for ai-ecosystem
export ANSIBLE_ROOT="/opt/architect_configs"
export GIT_REPO_SSH="git@github.com:Mrpongalfer/ai-ecosystem.git"
export GIT_REPO_HTTPS="https://github.com/Mrpongalfer/ai-ecosystem.git"
export PROJECT_BASE_DIR="$HOME/ai-ecosystem"
export SERVER_IP="192.168.0.95"
export CLIENT_IP="192.168.0.96"
export SSH_TARGET="pong@192.168.0.96"
# Use OpenLLaMA 7B (free) as our LLM for advanced recommendations.
export MODEL_NAME="openlm-research/open_llama_7b"
export DOCKER_IMAGE_TRAEFIK="traefik:latest"
echo "Elite configuration loaded."
