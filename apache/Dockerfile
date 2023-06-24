FROM httpd:latest

RUN apt update
RUN apt install -y vim python3
COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf
RUN apt install -y pip
RUN mkdir /root/.config
RUN mkdir /root/.config/pip
COPY ./pip.conf /root/.config/pip/
RUN pip install PyMySQL
RUN pip install requests
