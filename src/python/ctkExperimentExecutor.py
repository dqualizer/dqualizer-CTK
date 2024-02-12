from logzero import logger
from chaoslib import run, experiment
from chaoslib.types import Strategy, Journal
from flask import Flask, request, jsonify, make_response
import config
import mySqlConnector
from multiprocessing import Process, Queue
import json

app = Flask(__name__)


def run_experiment(chaos_experiment, result_queue):
    strategy: Strategy = Strategy.DEFAULT
    runner: run.Runner = run.Runner(strategy)
    result = None
    try:
        # Journal can be written to file (json) and transformed to experiment report document (pdf)
        journal: Journal = runner.run(chaos_experiment)
        # TODO TypeError: Object of type ValueError is not JSON serializable
        # Create file from journal. CAUTION: EXPOSES ENTERED SECRETS
        # with open(os.curdir, "w") as file:
        #     json.dump(journal, file)
        # logger.info(f"Experiment journal has been saved to {os.curdir}")
    except Exception as e:
        logger.error(e)
        result_dict = {"exit_code": 500,
                       "status": f"Experiment failed to execute.",
                       "errorTrace": e}
        result_json = json.dumps(result_dict)
        result_queue.put(result_json)

    result_dict = {
        "exit_code": 200,
        "status": "Experiment was executed successfully.",
        "errorTrace": ""
    }
    result_json = json.dumps(result_dict)
    result_queue.put(result_json)


# TODO Should be possible to ask for credentials here, so they not have to be sent by client --> NO TLS necessary for complete confidentiality!
# TODO We can now modify secrets in given experiment
@app.route('/execute_experiment', methods=['POST'])
def execute_experiment():
    request_headers = request.headers
    authentication_failed_json = jsonify({"exit_code": 401,
                                          "status": f"Authentication failed.",
                                          "errorTrace": ""})
    try:
        authentication_connection = mySqlConnector.create_db_connection(request_headers.get('dbUsername'),
                                                                        request_headers.get('dbPassword'))
    except Exception as e:
        logger.error(e)
        return authentication_failed_json

    try:
        authenticated = mySqlConnector.authenticate_user(authentication_connection, request_headers.get('username'),
                                                         request_headers.get('password'))
    except Exception as e:
        logger.error(e)
        return authentication_failed_json

    if not authenticated:
        logger.error("Failed to authenticate user!")
        return authentication_failed_json

    else:
        chaos_experiment = request.get_json()
        try:
            experiment.ensure_experiment_is_valid(chaos_experiment)
        except Exception as e:
            logger.error(e)
            return jsonify({"exit_code": 400,
                            "status": f"No valid experiment found.",
                            "errorTrace": e})

        result_queue = Queue()

        # Start a separate process to run the experiment to mitigate issues with signaling in main thread in chaoslib
        experiment_process = Process(target=run_experiment, args=(chaos_experiment, result_queue))
        experiment_process.start()

        # Wait for the experiment process to finish and send result to client
        experiment_process.join()
        response = make_response(result_queue.get())
        response.headers['Content-Type'] = 'application/json'

        return response



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='localhost', port=config.experiment_executor_api_port)
