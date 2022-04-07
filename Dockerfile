FROM python:slim-buster
RUN pip install virtualenv && \
    useradd githubuser
USER githubuser
COPY . /opt/manage-github-repo/
WORKDIR /opt/manage-github-repo/
RUN virtualenv venv && \
    source venv/bin/activate && \
    pip install -e /opt/manage-github-repo/
ENTRYPOINT ["/bin/bash"]
