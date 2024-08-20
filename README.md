# 📚 Linguatube

Learn english through watching Youtube

## Installation

Install the [LangChain CLI](https://pypi.org/project/langchain-cli/) if you haven't yet

```bash
pip install -U langchain-cli
```

Also, install [poetry](https://python-poetry.org/docs/) to manage packages

```bash
pip install poetry
```

Install packages
```bash
poetry install
```

## Environment Variable

This app requires several environment variables. Open the `.env-example`
file, rename it to .env, and complete the fields.

## Launch App

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.