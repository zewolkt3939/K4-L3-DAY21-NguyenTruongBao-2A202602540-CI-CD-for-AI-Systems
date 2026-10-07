#!/usr/bin/env bash
# Run on Ubuntu EC2 after uploading this repository to ~/income-app.
set -euo pipefail
bucket="${1:?Usage: bash scripts/setup_vm.sh BUCKET_NAME [AWS_REGION]}"
region="${2:-ap-southeast-1}"
app_dir="$HOME/income-app"
if [[ ! "$bucket" =~ ^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$ ]]; then
  echo 'Invalid S3 bucket name.' >&2
  exit 1
fi
if [[ ! "$region" =~ ^[a-z]{2}-[a-z]+-[0-9]+$ ]]; then
  echo 'Invalid AWS region.' >&2
  exit 1
fi
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip curl
cd "$app_dir"
python3 -m venv .venv
.venv/bin/python -m pip install --progress-bar off -r requirements-serve.txt
mkdir -p "$HOME/models"
sudo tee /etc/systemd/system/income-api.service >/dev/null <<EOF
[Unit]
Description=Adult Income Inference API
After=network-online.target
Wants=network-online.target

[Service]
User=$USER
WorkingDirectory=$app_dir
Environment="ARTIFACT_BUCKET=$bucket"
Environment="AWS_DEFAULT_REGION=$region"
Environment="MODEL_PATH=$HOME/models/model.joblib"
ExecStart=$app_dir/.venv/bin/python -m uvicorn src.serve:app --host 0.0.0.0 --port 8080
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
sudo tee /etc/sudoers.d/income-deploy >/dev/null <<EOF
$USER ALL=(root) NOPASSWD: /usr/bin/systemctl restart income-api, /usr/bin/journalctl -u income-api -n 30 --no-pager
EOF
sudo chmod 440 /etc/sudoers.d/income-deploy
sudo visudo -cf /etc/sudoers.d/income-deploy
sudo systemctl daemon-reload
sudo systemctl enable income-api
printf 'VM configured. The release workflow starts the service after publishing the model.\n'
