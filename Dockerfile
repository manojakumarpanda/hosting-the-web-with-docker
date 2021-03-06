FROM ubuntu:18.04
RUN apt-get -y update
Run apt update
RUN apt-get install -y supervisor
RUN apt-get install -y apache2 apache2-utils
RUN apt-get install -y libapache2-mod-wsgi-py3
#RUN mkdir -p /home/ubuntu/django/crm/logs
RUN mkdir -p /home/ubuntu/django/crm
RUN apt-get -y install python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install virtualenv
WORKDIR /home/ubuntu/django
RUN virtualenv -p python3 mmtxt
RUN chmod +x /home/ubuntu/django/
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./mysite-celery.conf /etc/supervisor/conf.d/crm-celery.conf
COPY ./requirements.txt /home/ubuntu/django/requirements.txt
#COPY ./files/* /home/ubuntu/django/crm
RUN mmtxt/bin/pip install -r /home/ubuntu/django/requirements.txt
#RUN chmod +x /home/ubuntu/django/crm

EXPOSE 80
COPY ./docker-entrypoint.sh /home/ubuntu/
RUN chmod +x /home/ubuntu/docker-entrypoint.sh
ENTRYPOINT ["/home/ubuntu/docker-entrypoint.sh"]