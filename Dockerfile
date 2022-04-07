FROM python:slim-bullseye
COPY . /opt/manage-github-repo/
RUN pip install --upgrade pip && \
    pip install -e /opt/manage-github-repo/
USER githubuser
WORKDIR /opt/manage-github-repo
ENTRYPOINT ["/bin/bash"]
