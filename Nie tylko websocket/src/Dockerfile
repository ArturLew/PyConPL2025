FROM python:3.13.7-slim as build-stage

WORKDIR /

ENV PDM_HOME=/root/.pdm
ENV PDM_CONFIG_SITE_PACKAGES=true
ENV PATH="/root/.pdm/bin:$PATH"
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONHASHSEED 1

RUN pip install pdm

COPY ./pyproject.toml ./
COPY ./pdm.lock ./

RUN pdm sync

COPY main_ext.py ./

CMD ["pdm", "run", "uvicorn", "main_ext:app", "--host", "0.0.0.0", "--port", "8000"]
