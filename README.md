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

Create/Synchronize the environment:

Go to the project directory and run the following command:

```bash
uv venv --python 3.11 --no-python-downloads --python-preference only-system
```

Add/remove packages to the environment (Ude --dev for development ONLY packages):

```bash
uv add <package>
uv remove <package>
```

Sync/Update packages in the environment:

```bash
uv sync --all-groups
uv lock --upgrade
```

Check package upgrades:

```bash
uv tree --outdated --all-groups
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
