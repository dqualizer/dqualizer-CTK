from logzero import logger
from chaoslib import run, experiment
from chaoslib.types import Strategy, Journal
from flask import Flask, request, jsonify
import config
import mySqlConnector

app = Flask(__name__)


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

        strategy: Strategy = Strategy.DEFAULT
        runner: run.Runner = run.Runner(strategy)
        try:
            # Journal can be written to file (json) and transformed to experiment report document (pdf)
            journal: Journal = runner.run(chaos_experiment)
        # TODO TypeError: Object of type ValueError is not JSON serializable
        except Exception as e:
            logger.error(e)
            return jsonify({"exit_code": 500,
                            "status": f"Experiment failed to execute.",
                            "errorTrace": e})

        # Create file from journal. CAUTION: EXPOSES ENTERED SECRETS
        # with open(os.curdir, "w") as file:
        #     json.dump(journal, file)
        # print(f"Experiment journal has been saved to {os.curdir}")

        return jsonify({"exit_code": 200,
                        "status": f"Experiment was executed successfully.",
                        "errorTrace": ""})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='localhost', port=config.experiment_executor_api_port)
