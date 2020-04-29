FROM python:3.8.2

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

RUN python get-pip.py

ADD bash_lib/develop.sh /bash_lib/develop.sh
ADD bash_lib/requirements.txt /bash_lib/requirements.txt
RUN bash /bash_lib/develop.sh