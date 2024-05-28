# Dqualizer-CTK (Resilience Execution API)

This is a project to integrate the [dqualizer project](https://github.com/dqualizer) with the [Chaos Toolkit (CTK)](https://github.com/chaostoolkit). This project enables the execution of CTK chaos experiments on the running host by providing an HTTP endpoint to receive CTK chaos experiment definitions.
We integrate functionality to execute [Chaos Monkey for Spring Boot](https://github.com/codecentric/chaos-monkey-spring-boot) actions and implement functionality to monitor and terminate local system processes. 
This project was created as part of my master's thesis, "Domain-Driven Resilience Testing of Business-Critical Application Systems" ([https://zenodo.org/records/10964241](https://zenodo.org/records/10964241)).

## Installation

### Prerequisites

- Python 3.11
- pip

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/LeHenningo/Dqualizer-CTK
   
2. Execute the `dqualizer_resilience_setup.sh` (If you also want to install the dqualizer project comment in lines 9-10)
3. Follow the hints echoed by `dqualizer_resilience_setup.sh`

If you want to use this API without dqualizer, you need to manually setup a MySQL database for authentication. 

## Start-Up

Start the Resilience Execution API by executing `python3 src/python/resilienceExecutionApi.py`.

## Endpoint Usage

Endpoint: `POST /execute_experiment`
Description: Validates and executes the supplied CTK chaos experiment.

### Authentication

To use the API, you need to authenticate using credentials for a MySQL database.

Include the credentials in the header of every request:
  ```plaintext
  "dbUsername": "aDBUser",
  "dbPassword": "aDBPw",
  "username": "demoUser",
  "password": "demo"
```

### Request
Header
```plaintext
POST /execute_experiment
Host: http://localhost:3323
Authorization:
  dbUsername: aDBUser,
  dbPassword: aDBPw,
  username: demoUser,
  password: demo
Content-Type: application/json
```
Body
```plaintext
{
  "title": "A new chaos experiment",
  "description": "This is a new chaos experiment",
  "method": ...
}
```
See [https://chaostoolkit.org/reference/api/experiment/](https://chaostoolkit.org/reference/api/experiment/) for the CTK chaos experiment structure.

### Response
```plaintext
{
  "status_code": "200",
  "title": "New Post",
  "status": "Experiment was executed and terminated with status: completed", 
  "info": "See Python logs, (experiment journal) and dashboards for result infos"
}
```



