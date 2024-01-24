import sys
import threading

from flask import Flask, request, jsonify
import os
import subprocess

import config


def print_output_and_accumulate(stream, prefix, accumulator):
    for line in iter(stream.readline, ''):
        accumulator += line
        sys.stdout.write(f"{prefix}: {line}")
        sys.stdout.flush()
    stream.close()


app = Flask(__name__)


@app.route('/execute_experiment', methods=['POST'])
def execute_experiment():
    experiment_filename = request.args.get('experiment_filename')
    journal_filename = request.args.get('journal_filename')

    if not experiment_filename:
        print("Experiment name not provided")
        return jsonify({"error": "Experiment name not provided"}), 400

    experiment_path = os.path.join(config.generated_experiments_volume_path, experiment_filename)
    journal_path = os.path.join(config.generated_experiments_volume_path, journal_filename)
    if not os.path.exists(experiment_path):
        print(f"There is no file existing at given path: {experiment_path}")
        return jsonify({"error": f"There is no file existing at given path: {experiment_path}"}), 400

    current_script_path = os.path.abspath(__file__)
    current_project_path = os.path.abspath(
        os.path.join(current_script_path, os.pardir, os.pardir, os.pardir))

    # Activate virtual environment to enable access to CTK lib
    # Path to the virtual environment's activation script (adjust depending on Windows or Linux)
    running_on_linux = os.name != "nt"
    if running_on_linux:
        venv_activate_script_path = os.path.join(current_project_path, "venv", "bin", "activate")
        # print(venv_activate_script_path)
        subprocess.run(["/bin/bash", "-c", f"source {venv_activate_script_path}"], check=True, capture_output=True, text=True)

    else:
        venv_activate_script_path = os.path.join(current_project_path, "venv", "Scripts", "activate")
        # print(venv_activate_script_path)
        subprocess.run([venv_activate_script_path], shell=True, check=True, capture_output=True, text=True)

    # result = subprocess.run(["echo", "a"], shell=True, check=True, capture_output=True, text=True)
    # result = subprocess.run(["pip", "list"], shell=True, check=True, capture_output=True, text=True)

    # subprocess.run(["set", f"PYTHONPATH={current_project_path}"], shell=True, check=True, capture_output=True, text=True)
    # subprocess.run(["echo", "%PYTHONPATH%"], shell=True, check=True, capture_output=True, text=True)

    # Setup python path environment variable to enable access to custom CTK scripts
    env = os.environ.copy()
    custom_modules_path = os.path.join(current_project_path, "src", "python")
    # print(custom_modules_path)
    env[
        "PYTHONPATH"] = f"{custom_modules_path}:{env.get('PYTHONPATH', '')}" if running_on_linux else f"{custom_modules_path};{env.get('PYTHONPATH', '')}"
    print("PYTHONPATH: " + env["PYTHONPATH"])

    # Run CTK experiment
    process = None
    print(f"Executing chaos run on {experiment_path}")
    if running_on_linux:
        process = subprocess.Popen(["chaos", "run", experiment_path, "--journal-path", journal_path],
                                   env=env,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

    else:
        process = subprocess.Popen(["chaos", "run", experiment_path, "--journal-path", journal_path],
                                   env=env,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

    # Lists to accumulate stdout and stderr logs from the subprocess (Strings are immutable)
    stdout_list = []
    stderr_list = []

    # Start separate threads to read stdout and stderr
    stdout_thread = threading.Thread(target=print_output_and_accumulate, args=(process.stdout, "stdout", stdout_list))
    stderr_thread = threading.Thread(target=print_output_and_accumulate, args=(process.stderr, "stderr", stderr_list))

    stdout_thread.start()
    stderr_thread.start()

    # Wait for the process to finish
    return_code = process.wait()

    # Wait for the output reading threads to finish
    stdout_thread.join()
    stderr_thread.join()

    # Convert the accumulated lists to strings
    stdout_str = ''.join(stdout_list)
    stderr_str = ''.join(stderr_list)

    return jsonify({"exit_code": return_code,
                    "status": f"Experiment at {experiment_path} was executed. See experiment journal at {journal_path}.",
                    "ctk_logs": stderr_str,
                    "custom_modules_logs": stdout_str})


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=config.experiment_executor_api_port)
