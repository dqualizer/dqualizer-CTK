from chaoslib import run
from chaoslib.types import Configuration, Secrets, Experiment, Hypothesis, Journal, Strategy
import chaosspring

experiment: Experiment = {
    "secrets":{"authentication":None},
    "title": "No description",
    "description": "No description",
    "method": [
        {
            "name": "enable_chaosmonkey",
            "provider": {
                "arguments": {
                    "base_url": "http://localhost:18080/actuator"
                },
                "func": "enable_chaosmonkey",
                "module": "chaosspring.actions",
                "type": "python"
            },
            "type": "action"
        },

        {
            "name": "configure_assaults",
            "provider": {
                "arguments": {
                    "base_url": "http://localhost:18080/actuator",
                    "assaults_configuration": {
                        "level": 1,
                        "deterministic": 'True',
                        "latencyRangeStart": 2000,
                        "latencyRangeEnd": 2000,
                        "latencyActive": 'True',
                        "exceptionsActive": 'False',
                        "killApplicationActive": 'False',
                        "restartApplicationActive": 'False',
                        "watchedCustomServices": [
                            "dqualizer.fibumock.stammdaten.zuordnung.ZuordnungService"
                        ]
                    }
                },
                "func": "change_assaults_configuration",
                "module": "chaosspring.actions",
                "type": "python"
            },
            "type": "action"
        },
        {
            "name": "configure_watcher",
            "type": "probe",
            "provider": {
                "type": "python",
                "module": "chaosspring.actions",
                "func": "change_watchers_configuration",
                "arguments": {
                    "base_url": "http://localhost:18080/actuator",
                    "watchers_configuration": {

                            "controller": 'False',
                            "restController": 'False',
                            "service": 'True',
                            "repository": 'False',
                            "component": 'False',
                            "restTemplate": 'False',
                            "webClient": 'False',
                            "actuatorHealth": 'False',
                            "beans": [],
                            "beanClasses": [],
                            "excludeClasses": []
                    }

                }
            }
        },

        {
            "name": "disable",
            "type": "probe",
            "provider": {
                "type": "python",
                "module": "chaosspring.actions",
                "func": "disable_chaosmonkey",
                "arguments": {
                    "base_url": "http://localhost:18080/actuator",
                }
            }
        }
    ]
}

#{"title":"No description","description":"No description","secrets":{"authentication":null},"steady-state-hypothesis":{"title":null,"probes":null},"method":[{"type":"action","name":"enable_chaosmonkey","provider":{"type":"python","module":"chaosspring.actions","func":"enable_chaosmonkey","arguments":{"base_url":"http://localhost:18080/actuator/actuator"}}},{"type":"action","name":"configure_assaults","provider":{"type":"python","module":"chaosspring.actions","func":"change_assaults_configuration","arguments":{"base_url":"http://localhost:18080/actuator/actuator","assault_configuration":{"level":1,"deterministic":true,"latencyRangeStart":2000,"latencyRangeEnd":2000,"latencyActive":true,"exceptionsActive":false,"killApplicationActive":false,"restartApplicationActive":false,"watchedCustomServices":[null]}}}},{"type":"action","name":"configure_watchers","provider":{"type":"python","module":"chaosspring.actions","func":"","arguments":{"base_url":"http://localhost:18080/actuator/actuator","watcher_configuration":{"controller":false,"restController":false,"service":false,"repository":false,"component":false,"restTemplate":false,"webClient":false,"actuatorHealth":false,"beans":[],"beanClasses":[],"excludeClasses":[]}}}}],"rollbacks":[{"type":"action","name":"disable_chaosmonkey","provider":{"type":"python","module":"chaosspring.actions","func":"disable_chaosmonkey","arguments":{"base_url":"http://localhost:18080/actuator/actuator"}}}]}

strategy: Strategy = Strategy.DEFAULT

runner: run.Runner = run.Runner(strategy)
journal: Journal = runner.run(experiment)
print(journal)
