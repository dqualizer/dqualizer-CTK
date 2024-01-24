#!/bin/bash
echo "=== Setting up Python venv in current directory ==="
python3 -m venv venv
source venv/bin/activate
echo "=== Installing Python dependencies in venv ==="
pip install -r requirements.txt
echo "=== Venv is now ready to run ctkExperimentExecutor and test-webserver. Please configurate config.py before you start the scripts, e.g. 'python3 ctkExperimentExecutor.py'. ==="
echo "=== Now starting to clone dqualizer repository in parent directory ==="
cd ..
git clone https://github.com/dqualizer/dqualizer.git
echo "=== Finished cloning dqualizer repo in parent dir. Please enter dqualizer dir 'cd ../dqualizer' and 'git checkout Resilience' to check the docker-compose.yml. After that you are good to 'docker-compose up'. ==="