FROM python:2-onbuild

RUN apt-get update
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN ln -sf `which nodejs` /usr/bin/node

WORKDIR "/usr/src/app/billing-app"

RUN npm install -g grunt-cli
RUN npm install
RUN grunt
EXPOSE "8080"
CMD /usr/local/bin/gunicorn wsgi:app -w 5 -b :8080 --error-logfile ./gunicorn.log