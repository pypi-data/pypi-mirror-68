FROM debian:latest
RUN apt-get update && \
	apt-get install pylint3 python3-pip tox git \
	curl pycodestyle  -y
ARG COMMIT="dev"
RUN git clone -b dev https://gitlab.com/caosdb/caosdb-pylib.git && \
    cd caosdb-pylib && git checkout $COMMIT && pip3 install .
