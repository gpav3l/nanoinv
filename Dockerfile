# set the base image 
FROM nginx:1.21.6

ENV DEP_PORT=8090

RUN apt update
RUN apt install -y python3 \
python3-pip  uwsgi uwsgi-plugin-python3 \
nano

WORKDIR /usr/share/nginx/html
COPY ./invbase ./
COPY ./django.ini /etc/uwsgi/apps-enabled/
COPY ./django.conf /etc/nginx/conf.d/default.conf

#set directoty where CMD will execute 
RUN chown -R www-data:www-data */

COPY requirements.txt ./

# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Expose ports
EXPOSE $DEP_PORT

# default command to execute    
CMD service uwsgi start & service nginx start & while true; do sleep 2; done
