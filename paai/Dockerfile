ARG PYTHON_VERSION=3.8.5-slim
FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for installing poetry
    curl \
    git \
    nano \
    ssh \
    # dependencies for building python dependencies
    build-essential \
    && rm -rf /var/lib/apt/lists/*


ENV POETRY_HOME="/.poetry"
# make poetry available
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /usr/src/app

COPY pyproject.toml .
COPY poetry.lock .

COPY paai ./paai
COPY tests ./tests
RUN poetry install

CMD ["poetry", "run", "python", "paai/main.py"]