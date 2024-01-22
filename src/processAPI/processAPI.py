from flask import Flask, request, jsonify
from datetime import datetime
import psutil

app = Flask(__name__)


@app.route('/check_process', methods=['GET'])
def get_process_exists():
    process_name = request.args.get('name')

    if not process_name:
        return jsonify({"error": "Process name not provided"}), 400

    print(f"checking for process {process_name} " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Check is Case-sensitive!
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            print(f"process {process_name} exists " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return jsonify({f"{process_name} exists": True})

    print(f"process {process_name} was not found " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({f"{process_name} exists": False})


@app.route('/kill_process', methods=['POST'])
def kill_process_endpoint():
    process_name = request.args.get('name')
    # Kill is Case-sensitive!
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            try:
                psutil.Process(process.info['pid']).terminate()
                return jsonify({"status": f"Process {process_name} killed successfully"})
            except Exception as e:
                return jsonify({"error": f"Error killing process: {str(e)}"}), 500

    return jsonify({"error": f"Process {process_name} was not found and could not be killed"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=443)
