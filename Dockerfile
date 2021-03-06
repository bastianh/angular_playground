FROM python:3.4
RUN curl -sL https://deb.nodesource.com/setup | bash - && apt-get install -y supervisor nodejs nginx

ADD . /code
WORKDIR /code
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN npm install
RUN npm run build

CMD ["/usr/bin/supervisord", "-c", "/code/config/supervisord.conf"]
