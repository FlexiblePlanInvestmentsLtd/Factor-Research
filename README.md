# Factor-Research

Factor Research using machine learning

## Setup

### UV Python Environment Manager

* First Install UV Python Environment Manager: [Link](https://docs.astral.sh/uv/)  
* Access the UV documentation: [Link](https://docs.astral.sh/uv/)

Installation:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### VSode

* Python Data Science Extension Pack: [Link](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.python-ds-extension-pack)  
* Ruff Extension for Linting and Formatting: [Link](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)  
* MyPy Extension for Type Checking: [Link](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)  

## Environment Setup

Use .env_example create .env file and fill in the required environment variables. Use [Python-Dotenv](https://pypi.org/project/python-dotenv/) to create a virtual environment.

| Key                               | Description                        |
| --------------------------------- | ---------------------------------- |
| FACTOR_RESEARCH_EOD_HD_API_KEY    | EOD Data Providers API Key         |
