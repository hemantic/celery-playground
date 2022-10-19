FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update && \
  apt-get --no-install-recommends --assume-yes install  \
  # build tools
	nasm \
	build-essential \
	autoconf \
	automake \
	libtool \
	pkg-config \
  git \
  zlib1g-dev \
  # cleanup
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install python packages
COPY src/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install uwsgi
RUN pip install --no-cache-dir -r requirements.txt

ADD src /srv

WORKDIR /srv
