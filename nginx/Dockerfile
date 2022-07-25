FROM nginx

ADD ./nginx/site.conf /etc/nginx/conf.d/default.conf
ADD ./nginx/uwsgi_params /etc/nginx/uwsgi_params
ADD ./nginx/static /etc/nginx/static

RUN mkdir -p /var/www/public/
ADD ./frontend/dist /var/www/public