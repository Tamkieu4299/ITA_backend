# backend

    - Python version: 3.11
    - pip verison: 22.3

## Project structure

```
ITA-APP-SERVER
└───src
|   ├───service1             # One Service in Microservices Structure
|   │   └───app
|   │   |   ├───crud         # crud services
|   │   |   ├───db           # database connection and config
|   │   |   ├───models       # db models
|   │   |   ├───routers
|   │   |   ├───schemas      # pydantic models
|   │   |   ├───constants    # local configs
|   │   |   ├───utils        # local utils such as logging module
|   │   |   ├───api.py
|   │   |   ├───Dockerfile
|   │   |   ├───poetry.lock
|   │   |   ├───pyproject.toml
|   |   |___logs             # include log files
|   ├───service2
|   │   └───app
|   │   |   ├───...
```

## Setup

Copy from `.env-example` to `.env` and fill the placeholder. The server configuration can be find at [here](https://deltacognition.sharepoint.com/:t:/s/ITA-IntelligentTalentAllocation-TechHub/EeoEvefN-59EqEKNdRv_avMBuupGShZp4dxIzxiWejSs5A?e=z8VDak).

## Build & Run

### Production

If you are on Linux or macOS, please run the following command.

    ./scripts/run-prod

### Development

If you are about to add new dependencies during the development, please follow **all** the steps below. If there is no need to add a new dependency, please follow from **Step 5** to **Step 6**.

1. Follow steps in this [website](https://docs.conda.io/en/latest/miniconda.html#installing) to install MiniConda.
2. Run the following commands

```shell
# Create a virtual environment
conda create -n ita-app-server python=3.11
# Activate the virtual environment
conda activate ita-app-server
```

3. Follow steps in this [website](https://python-poetry.org/docs/#installation) to install Poetry.
4. Install all dependencies

```
poetry install
```

5. Install pre-commit

```
pre-commit install
```

6. (Optional) Add a new dependency

Navigate to the directory of the service where you want to add a new dependency.

```shell
# If the dependency for both development and production
poetry add [dependency-name]
# If the dependency only for development
poetry add -D [dependency-name]
```

7. Run Docker containers

If you are on Linux or macOS, please run the following command.

    ./scripts/run-dev

### Variables for Testing purpose:
1. Currently, we do not implement Authentication feature, so the user_id will be a dummy data:

    dummy_user_id = [
        "9e7c97ef-af04-44b2-b36b-a65070b88abc",
        "7da2ca29-9bff-447d-bcff-c77e7bba8eab",
        "26e659d1-59f8-44b9-9b3d-c3d67b3a6b51",
        "b2f27dfc-55d8-47f6-9fa0-3b6d448f6df8",
        "e7864312-c27f-4327-ba92-9bf86bdcf367",
    ]

    This variable is put in the /studio/src/app/services/validate_data.py for checking the valid user
