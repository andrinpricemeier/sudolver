# syntax = docker/dockerfile:1.4.2

# Install YOLO and its requirements in a virtual env so that the dependencies are easier to copy to the final stage.
FROM python:3.7 AS yolo-deps
RUN git clone https://github.com/ultralytics/yolov5 /sudolver/yolov5
WORKDIR /sudolver/yolov5
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Install PDM dependencies
# PDM doesn't support libraries such as pytorch yet, that's why there are two ways of installing dependencies.
FROM python:3.7 AS sudolver-deps
RUN pip install --no-cache-dir -U pip==22.1 setuptools==62.2.0 wheel==0.37.1 && pip install --no-cache-dir pdm==1.15.0
COPY pyproject.toml pdm.lock /sudolver/
WORKDIR /sudolver
RUN pdm install --prod --no-lock --no-editable

FROM python:3.7-slim AS base-python
RUN  export DEBIAN_FRONTEND=noninteractive \
 && apt-get update \
 && apt-get -y upgrade \
 && apt-get install --no-install-recommends ffmpeg=7:4.3.4-0+deb11u1 tini=0.19.0-1 -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password --gecos '' --uid 1001 --shell /bin/false user

FROM base-python
# Make packages available to our server.
ENV PYTHONPATH=/sudolver/pkgs
ENV PATH="/opt/venv/bin:$PATH"
# Get notified of C segfaults
ENV PYTHONFAULTHANDLER=1
# Copy over dependencies, models and code.
COPY --chown=user:user --from=yolo-deps /opt/venv /opt/venv
COPY --chown=user:user --from=sudolver-deps /sudolver/__pypackages__/3.7/lib /sudolver/pkgs
COPY --chown=user:user --from=yolo-deps /sudolver/yolov5 /sudolver/yolov5
COPY --chown=user:user trained_model/ /sudolver/trained_model
COPY --chown=user:user app/ /sudolver/app
COPY --chown=user:user .env /sudolver/
USER user
WORKDIR /sudolver
EXPOSE 8080
# Precompile python code to reduce startup time.
RUN python -m compileall app/
CMD ["tini", "-g", "--", "python", "-m", "app.main"]