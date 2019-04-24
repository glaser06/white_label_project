# start from base
FROM ubuntu:14.04
MAINTAINER Prakhar Srivastav <prakhar@prakhar.me>

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -yq nodejs

# copy our application code
ADD app /opt/app
WORKDIR /opt/app

# fetch app specific deps

RUN pip install -r requirements.txt

# expose port
EXPOSE 5000

# start app
CMD [ "python", "scenes/api/endpoints.py" ]