FROM nginx:latest

ADD ./deploy /code
RUN chown -R root:nginx /code \
    && chmod -R 440 /code \
    && chmod 550 /code
