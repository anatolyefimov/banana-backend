FROM nginx:latest

RUN rm -rf /etc/nginx/conf.d/default.conf

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]