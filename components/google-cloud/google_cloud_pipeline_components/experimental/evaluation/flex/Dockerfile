# A container for model evaluation.

FROM python:3.8

RUN python --version

WORKDIR .
ADD *.py /
ADD requirements.txt /
ADD lib/*.py /lib/

ENV FLEX_TEMPLATE_PYTHON_PY_FILE "/main.py"
ENV FLEX_TEMPLATE_PYTHON_PY_OPTIONS ""
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE "/setup.py"

# Global for reuse elsewhere.
#
ENV REQUIREMENTS_FILE "/requirements.txt"
RUN cat "${REQUIREMENTS_FILE}"
RUN pip install --upgrade pip
RUN pip install -U -r "${REQUIREMENTS_FILE}"
