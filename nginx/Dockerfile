FROM nginx:1.25.5-alpine
COPY ./nginx/config.conf /etc/nginx/conf.d/default.conf
COPY ./MesSenderFront/mes-sender/build /var/www/html
EXPOSE 80