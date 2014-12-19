FROM ubuntu

MAINTAINER Florent Espanet <florent.esp@gmail.com>

# Dependencies
RUN apt-get update
RUN apt-get install -y git unzip wget net-tools build-essential
RUN apt-get install -y python python-dev python-distribute python-pip

# Add the application to the docker instance
ADD sleekstatus /sleekstatus/
WORKDIR /sleekstatus/

# Forward the web port
EXPOSE 5000

# Install the application
RUN pip install -e /sleekstatus/