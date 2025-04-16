#!/bin/bash
# continue_project.sh
# ----------------------------------------------------------
# This script continues with the complete integration
# of your autonomous AI ecosystem project.
#
# It does the following:
#   1. Sources elite configuration settings from elite_config.sh.
#   2. Updates (or clones, if necessary) your Ansible playbooks from your GitHub repo,
#      located in /opt/architect_configs.
#   3. Verifies that Docker and Docker Compose (or plugin) are installed.
#   4. Checks for any running Traefik containers.
#   5. Activates the project's virtual environment and launches the deployment script.
#
# All of this follows elite-tier best practices to integrate your existing work
# with the new AI ecosystem components.
# ----------------------------------------------------------

# Source our elite configuration settings.
source "$HOME/ai-ecosystem/elite_config.sh"

echo "--------------------------------------------------"
echo "Updating Ansible playbooks at $ANSIBLE_ROOT ..."
if [ -d "$ANSIBLE_ROOT" ]; then
  sudo git -C "$ANSIBLE_ROOT" pull || { echo "[ERROR] Failed to pull latest changes from Ansible repo."; exit 1; }
else
  echo "[INFO] $ANSIBLE_ROOT does not exist. Cloning repository using SSH..."
  sudo git clone "$GIT_REPO_SSH" "$ANSIBLE_ROOT" || { echo "[ERROR] Git clone failed."; exit 1; }
fi
echo "--------------------------------------------------"
echo "Ansible playbooks updated."

echo "--------------------------------------------------"
echo "Verifying Docker installation..."
if command -v docker &> /dev/null; then
    echo "[INFO] Docker is installed: $(docker --version)"
else
    echo "[ERROR] Docker is not installed. Please install Docker and re-run this script."
    exit 1
fi
echo "--------------------------------------------------"

echo "Verifying Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "[INFO] docker-compose is installed: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    echo "[INFO] Docker Compose plugin is available (via 'docker compose')."
else
    echo "[ERROR] Docker Compose is not installed. Please install docker-compose."
    exit 1
fi
echo "--------------------------------------------------"

echo "[INFO] Checking for running Traefik containers..."
docker ps --filter "ancestor=$DOCKER_IMAGE_TRAEFIK" || echo "[INFO] No Traefik container found."
echo "--------------------------------------------------"

echo "Activating the virtual environment..."
source "$PROJECT_BASE_DIR/venv/bin/activate" || { echo "[ERROR] Virtual environment activation failed."; exit 1; }

echo "Deploying the Autonomous AI Ecosystem..."
python3 "$PROJECT_BASE_DIR/scripts/deploy_agents.py" || { echo "[ERROR] Deployment script failed."; exit 1; }

echo "--------------------------------------------------"
echo "Deployment complete. Your AI ecosystem is now running."
echo "Remember: To work on this project in the future, use:" 
echo "   source $PROJECT_BASE_DIR/venv/bin/activate"
