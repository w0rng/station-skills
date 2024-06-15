FROM python:3.11-slim AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY /src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

# run stage
FROM python:3.11-slim

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs

# retrieve executables
COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/

# add source code
COPY --from=builder /project/src /project/src
WORKDIR /project/src

# expose the port the app runs on
EXPOSE 8080

# command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
