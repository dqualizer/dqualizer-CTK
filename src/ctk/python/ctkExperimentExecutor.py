import sys

from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)


@app.route('/execute_experiment', methods=['POST'])
def execute_experiment():
    experiment_path = request.args.get('experiment_path')
    # CTK logs experiment in journal path
    journal_path = request.args.get('journal_path')

    # if not experiment_path:
    #     print("Path to experiment not provided")
    #     return jsonify({"error": "Path to experiment not provided"}), 400

    # if not os.path.exists(experiment_path):
    #     print(f"There is no file existing at given path: {experiment_path}")
    #     return jsonify({"error": f"There is no file existing at given path: {experiment_path}"}), 400

    print(f"Executing chaos run on {experiment_path}")
    current_script_path = os.path.abspath(__file__)
    print(current_script_path)
    current_project_path = os.path.abspath(os.path.join(current_script_path, os.pardir, os.pardir, os.pardir, os.pardir))
    print(current_project_path)

    # Path to the virtual environment's activation script (adjust depending on Windows or Linux)
    venv_activate_script_path = os.path.join(current_project_path, "venv", "bin", "activate") if os.name != "nt" else os.path.join(current_project_path, "venv", "Scripts", "activate")
    print(venv_activate_script_path)
    subprocess.run([venv_activate_script_path], shell=True, check=True, capture_output=True, text=True)
    #print(result)
    result = subprocess.run(["echo", "a"], shell=True, check=True, capture_output=True, text=True)
    result = subprocess.run(["echo", "%PYTHONPATH%"], shell=True, check=True, capture_output=True, text=True)
    print(result)
    #result = subprocess.run(["chaos", "run", experiment_path, "--journal-path", journal_path], capture_output=True, text=True)
    #result = subprocess.run(["chaos", "run"])

    print("Chaos Toolkit Output:")
    #print(result.stdout)
    #print(result.stderr)
    resultCTK = subprocess.run([sys.executable, "-m", "chaos", "run"], shell=True, check=True)
    print(resultCTK)

   # if result.returncode != 0:
    #    print("Error executing chaos run:")
    #     print(result.stderr)
    #     return jsonify({"status": f"Experiment at {experiment_path} was executed and resulted in code {result.returncode}. See experiment journal at {journal_path}."})
    #
    # return jsonify({"status": f"Experiment at {experiment_path} was successfully executed. See experiment journal at {journal_path}."})


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3323)
