FROM python:3.4
RUN curl -sL https://deb.nodesource.com/setup | bash - && apt-get install -y supervisor nodejs nginx


#ADD . /code
ADD requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt

CMD ["/usr/bin/supervisord", "-c", "/code/config/supervisord.conf"]
