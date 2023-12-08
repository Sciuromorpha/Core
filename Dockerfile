FROM python:3.11-slim

ARG SCIUROMORPHA_MODE=development
ARG UID="1998"
ARG GID="1998"

ENV SCIUROMORPHA_MODE=${SCIUROMORPHA_MODE}\
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    # brotli \
    build-essential \
    tini \
    # curl \
    # gettext \
    # git \
    # libpq-dev
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists \
    && pip install "poetry==$POETRY_VERSION" 
    # && groupadd -g "${GID}" sciuromorpha \
	# && useradd -l -u "${UID}" -g "${GID}" -m -d /app sciuromorpha


# Copy only requirements to cache them in docker layer
# USER sciuromorpha
WORKDIR /app
COPY . /app
# COPY poetry.lock pyproject.toml /app/

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
    echo "$SCIUROMORPHA_MODE" \
    && poetry version \
    # Install deps:
    && poetry run pip install -U pip \
    && poetry install \
    $(if [ "$SCIUROMORPHA_MODE" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["faststream", "run", "sciuromorpha_core:app"]
