#!/bin/bash
echo "=== Setting up Python venv in current directory ==="
python3 -m venv venv
source venv/bin/activate
echo "=== Installing Python dependencies in venv ==="
pip install -r requirements.txt
echo "=== Venv is now ready to run ctkExperimentExecutor and test-webserver. ==="
echo "=== Now starting to clone dqualizer repository in parent directory ==="
cd ..
git clone https://github.com/dqualizer/dqualizer.git
echo "=== Finished cloning dqualizer repo in parent dir. Please enter dqualizer dir 'cd ../dqualizer' and 'git checkout Resilience' to check the docker-compose.yml. After that you are good to 'docker-compose up'. ==="
echo "=== 1. TODO for you: check config 'nano /src/python/config.py'; activate venv 'source venv/bin/activate'); start ctk-API on your host machine 'python3 src/python/ctkExperimentExecutor.py' ==="
echo "=== 2. TODO for you: move to dqualizer repo 'cd ../dqualizer'; checkout resilience branch 'git checkout Resilience'; check docker-compose.yml 'nano docker-compose.yml'; start up dqualizer 'docker-compose up' ==="