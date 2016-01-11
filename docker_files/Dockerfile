FROM ubuntu:14.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get install -y  git

RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/blaze/distributed.git

RUN pip install futures

RUN pip install git+https://github.com/blaze/distributed.git@master --upgrade

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

CMD [ "/bin/bash" ]


