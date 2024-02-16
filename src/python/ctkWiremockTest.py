from chaoslib import run
from chaoslib.types import Configuration, Secrets, Experiment, Hypothesis, Journal, Strategy
import chaoswm

experiment: Experiment = {"configuration": {
    "wiremock": {
        "host": "localhost",
        "port": 8082,
        "contextPath": "",
        "timeout": 10,
        "down": {
            "type": "lognormal",
            "median": 3000,
            "sigma": 0.2
        }
    }
},
    "title": "No description",
    "description": "No description",
    "method": [
        {
            "type": "action",
            "name": "Adding a fixed delay to a mapping",
            "provider": {
                "type": "python",
                "module": "chaoswm.actions",
                "func": "fixed_delay",
                "arguments": {
                    "filter": [{
                        "method": "GET",
                        "url": "/.*"
                    }],
                    "fixedDelayMilliseconds": 1000
                }
            }
        }
    ]
}

strategy: Strategy = Strategy.DEFAULT

runner: run.Runner = run.Runner(strategy)
journal: Journal = runner.run(experiment)
print(journal)
