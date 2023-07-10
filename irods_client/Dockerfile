FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        apt-transport-https \
        gnupg \
        wget \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

RUN wget -qO - https://packages.irods.org/irods-signing-key.asc | apt-key add - && \
    echo "deb [arch=amd64] https://packages.irods.org/apt/ focal main" | tee /etc/apt/sources.list.d/renci-irods.list

ARG icommands_version=4.3.0
ARG icommands_package_version_suffix=-1~focal
ARG icommands_package_version=${icommands_version}${icommands_package_version_suffix}

RUN apt-get update && \
    apt-get install -y \
        irods-icommands=${icommands_package_version} \
        netcat \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

RUN mkdir -p /root/.irods
COPY irods_environment.json /root/.irods
RUN mkdir -p /root/.ibridges
COPY ibridges_config.json /root/.ibridges
RUN mkdir -p /tmp
ADD testdata /tmp/testdata/

# install python 3
RUN apt-get update && \
    apt-get upgrade -y
RUN apt-get install -y python3 \
	python3-pip \
	git

ADD iBridges-Gui /iBridges-Gui/
COPY requirements.txt /iBridges-Gui/requirements_docker.txt
RUN pip3 install -r /iBridges-Gui/requirements_docker.txt
COPY integration_test.py /iBridges-Gui/integration_test.py

WORKDIR /
COPY entrypoint.sh .
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT bash -c "./entrypoint.sh"
