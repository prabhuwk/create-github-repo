FROM python:slim-buster
COPY . /opt/manage-github-repo/
RUN pip install -e /opt/manage-github-repo/ && \
    useradd githubuser
USER githubuser
WORKDIR /opt/manage-github-repo/
ENTRYPOINT ["/bin/bash"]