from chaoslib import run, experiment
from chaoslib.types import Configuration, Secrets, Experiment, Hypothesis, Journal, Strategy
import chaosspring

chaos_experiment: Experiment = {
    "title": "ResilienceTest1716200537983",
    "description": "ResilienceTestDescription",
    "secrets": {
        "authentication": {
            "username": "demoUser",
            "password": "demo",
            "db_username": "aDBUser",
            "db_password": "aDBPw"
        }
    },
    "steady-state-hypothesis": {
        "title": "Application is running",
        "probes": [
            {
                "type": "probe",
                "name": "leasingninja-riskApi-0.0.1 must be running",
                "provider": {
                    "type": "python",
                    "module": "processMonitoring",
                    "func": "check_process_exists",
                    "arguments": {
                        "db_username": "${db_username}",
                        "db_password": "${db_password}",
                        "username": "${username}",
                        "password": "${password}",
                        "process_name": "leasingninja-riskApi-0.0.1",
                        "log_result_in_influx_db": True
                    }
                },
                "tolerance": True
            }
        ]
    },
    "method": [
        {
            "type": "action",
            "name": "kill process leasingninja-riskApi-0.0.1",
            "provider": {
                "type": "python",
                "module": "processKilling",
                "func": "kill_process_by_name",
                "arguments": {
                    "db_username": "${db_username}",
                    "db_password": "${db_password}",
                    "username": "${username}",
                    "password": "${password}",
                    "process_name": "leasingninja-riskApi-0.0.1"
                }
            },
            "pauses": {
                "before": 5,
                "after": 0
            }
        },
        {
            "type": "probe",
            "name": "measure duration until process leasingninja-riskApi-0.0.1 is eventually available again",
            "provider": {
                "type": "python",
                "module": "processMonitoring",
                "func": "get_duration_until_process_started",
                "arguments": {
                    "db_username": "${db_username}",
                    "db_password": "${db_password}",
                    "username": "${username}",
                    "password": "${password}",
                    "process_name": "leasingninja-riskApi-0.0.1",
                    "monitoring_duration_sec": 10,
                    "checking_interval_sec": 0
                }
            }
        }
    ],
    "rollbacks": [
        {
            "type": "action",
            "name": "start process leasingninja-riskApi-0.0.1",
            "provider": {
                "type": "python",
                "module": "processStarting",
                "func": "start_process_by_path",
                "arguments": {
                    "db_username": "${db_username}",
                    "db_password": "${db_password}",
                    "username": "${username}",
                    "password": "${password}",
                    "path": None,
                    "log_result_in_influx_db": True
                }
            }
        }
    ],
    "extensions": [
        {
            "name": "expected response measures",
            "expected_recovery_time_ms": 500
        }
    ],
    "runtime": {
        "rollbacks": {
            "strategy": "deviated"
        }
    }
}

# {"title":"No description","description":"No description","secrets":{"authentication":null},"steady-state-hypothesis":{"title":null,"probes":null},"method":[{"type":"action","name":"enable_chaosmonkey","provider":{"type":"python","module":"chaosspring.actions","func":"enable_chaosmonkey","arguments":{"base_url":"http://localhost:18080/actuator/actuator"}}},{"type":"action","name":"configure_assaults","provider":{"type":"python","module":"chaosspring.actions","func":"change_assaults_configuration","arguments":{"base_url":"http://localhost:18080/actuator/actuator","assault_configuration":{"level":1,"deterministic":true,"latencyRangeStart":2000,"latencyRangeEnd":2000,"latencyActive":true,"exceptionsActive":false,"killApplicationActive":false,"restartApplicationActive":false,"watchedCustomServices":[null]}}}},{"type":"action","name":"configure_watchers","provider":{"type":"python","module":"chaosspring.actions","func":"","arguments":{"base_url":"http://localhost:18080/actuator/actuator","watcher_configuration":{"controller":false,"restController":false,"service":false,"repository":false,"component":false,"restTemplate":false,"webClient":false,"actuatorHealth":false,"beans":[],"beanClasses":[],"excludeClasses":[]}}}}],"rollbacks":[{"type":"action","name":"disable_chaosmonkey","provider":{"type":"python","module":"chaosspring.actions","func":"disable_chaosmonkey","arguments":{"base_url":"http://localhost:18080/actuator/actuator"}}}]}

experiment.ensure_experiment_is_valid(chaos_experiment)
strategy: Strategy = Strategy.DEFAULT

runner: run.Runner = run.Runner(strategy)

settings = {}
if chaos_experiment.get("runtime"):
    settings["runtime"] = chaos_experiment.get("runtime")

journal: Journal = runner.run(chaos_experiment, settings)
print(journal)
