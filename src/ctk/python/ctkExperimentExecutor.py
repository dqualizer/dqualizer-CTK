import sys

from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

generated_experiments_volume_path = "C:\\Users\\HenningMöllers\\IdeaProjects\\dqualizer\\docker-output\\generated_experiments"


@app.route('/execute_experiment', methods=['POST'])
def execute_experiment():
    experiment_filename = request.args.get('experiment_filename')
    # CTK logs experiment in journal path
    journal_filename = request.args.get('journal_filename')

    if not experiment_filename:
        print("Experiment name not provided")
        return jsonify({"error": "Experiment name not provided"}), 400

    experiment_path = os.path.join(generated_experiments_volume_path, experiment_filename)
    journal_path = os.path.join(generated_experiments_volume_path, journal_filename)
    if not os.path.exists(experiment_path):
        print(f"There is no file existing at given path: {experiment_path}")
        return jsonify({"error": f"There is no file existing at given path: {experiment_path}"}), 400

    print(f"Executing chaos run on {experiment_path}")
    current_script_path = os.path.abspath(__file__)
    # print(current_script_path)
    current_project_path = os.path.abspath(
        os.path.join(current_script_path, os.pardir, os.pardir, os.pardir, os.pardir))
    # print(current_project_path)

    # Path to the virtual environment's activation script (adjust depending on Windows or Linux)
    runningOnLinux = os.name != "nt"
    venv_activate_script_path = os.path.join(current_project_path, "venv", "bin",
                                             "activate") if runningOnLinux else os.path.join(current_project_path,
                                                                                             "venv", "Scripts",
                                                                                             "activate")
    # print(venv_activate_script_path)

    # result = subprocess.run(["echo", "a"], shell=True, check=True, capture_output=True, text=True)
    # result = subprocess.run(["pip", "list"], shell=True, check=True, capture_output=True, text=True)

    try:
        subprocess.run([venv_activate_script_path], shell=True, check=True, capture_output=True, text=True)
        # subprocess.run(["set", f"PYTHONPATH={current_project_path}"], shell=True, check=True, capture_output=True, text=True)
        # subprocess.run(["echo", "%PYTHONPATH%"], shell=True, check=True, capture_output=True, text=True)
        env = os.environ.copy()
        custom_modules_path = os.path.join(current_project_path, "src", "ctk", "python")
        print(custom_modules_path)
        env[
            "PYTHONPATH"] = f"{custom_modules_path}:{env.get('PYTHONPATH', '')}" if runningOnLinux else f"{custom_modules_path};{env.get('PYTHONPATH', '')}"
        print("PYTHONPATH: " + env["PYTHONPATH"])
        subprocess.run(["chaos", "run", experiment_path, "--journal-path", journal_path], env=env, shell=True,
                       check=True, capture_output=True,
                       text=True)
        # result = subprocess.run(["python", "-c", "import sys; print(sys.path)"], env=env, shell=True, check=True,
        #                capture_output=True, text=True)
        # print(result)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"stderr: {e.stderr}")
        return jsonify({"exit_code": e.returncode,
                        "status": f"Experiment at {experiment_path} was executed and resulted in code {e.returncode}, {e.stderr}."})

    return jsonify({"exit_code": 0,
                    "status": f"Experiment at {experiment_path} was successfully executed. See experiment journal at {journal_filename}."})


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3323)
