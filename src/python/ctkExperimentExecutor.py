import os

from logzero import logger
from chaoslib import run, experiment
from chaoslib.types import Strategy, Journal
from flask import Flask, request, jsonify, make_response
import config
import influxDBConnector
import mySqlConnector
from multiprocessing import Process, Queue
import json

app = Flask(__name__)


def run_experiment(chaos_experiment, result_queue):
    strategy: Strategy = Strategy.DEFAULT
    runner: run.Runner = run.Runner(strategy)
    journal = {}
    try:
        # Journal can be written to file (json) and transformed to experiment report document (pdf)
        journal: Journal = runner.run(chaos_experiment)
        # Create file from resulting journal. CAUTION: EXPOSES ENTERED SECRETS WHEN SECRETS WERE DEFINED INLINE,
        # comment out for production use
        journal_path = os.path.join(os.curdir, "journal.json")
        with open(journal_path, "w") as file:
            json.dump(journal, file, indent=4)
            logger.info(f">>>>>>> Experiment journal has been saved to {journal_path}")
    except Exception as e:
        logger.error(e)
        result_dict = {"status_code": 500,
                       "status": f"Experiment failed to execute and thrown exception was not caught by CTK.",
                       "info": e}
        result_json = json.dumps(result_dict)
        result_queue.put(result_json)

    result_dict = {
        # TODO wrongly returns 'completed' if rollback fails!
        # throws also 500 status if the experiment terminated with status 'deviated'
        "status_code": 200 if journal["status"] == "completed" else 500,
        "status": f"Experiment was executed and terminated with status: {journal["status"]}.",
        "info": "See Python logs, (experiment journal) and dashboards for result infos"
    }
    result_json = json.dumps(result_dict)
    result_queue.put(result_json)


@app.route('/execute_experiment', methods=['POST'])
def execute_experiment():
    request_headers = request.headers
    authentication_failed_json = jsonify({"status_code": 401,
                                          "status": f"Authentication failed.",
                                          "info": ""})
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
        # Create file from experiment. CAUTION: EXPOSES ENTERED SECRETS WHEN SECRETS WERE DEFINED INLINE, comment out
        # for production use
        experiment_path = os.path.join(os.curdir, "experiment.json")
        with open(experiment_path, "w") as file:
            json.dump(chaos_experiment, file, indent=4)
            logger.info(f">>>>>>> Received chaos experiment has been saved to {experiment_path}")
        try:
            experiment.ensure_experiment_is_valid(chaos_experiment)
        except Exception as e:
            logger.error(e)
            return jsonify({"status_code": 400,
                            "status": f"No valid experiment found.",
                            "info": e})

        # only considers one defined response measure at the moment, as it is not possible to define multiple at the moment
        # TODO add cases for other resilience response measures 'expected_error_rate_percent', 'expected_response_time_ms'
        extensions = chaos_experiment.get('extensions', None)
        if extensions is not None:
            response_measure_extension = chaos_experiment['extensions'][0]
            expected_recovery_time = response_measure_extension.get('expected_recovery_time_ms', None)
            if expected_recovery_time is not None:
                influxDBConnector.write_monitoring_data("expected_response_measure", "",
                                                        "",
                                                        'expected_recovery_time',
                                                        expected_recovery_time)

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
