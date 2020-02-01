FROM devilbox/php-fpm:7.4-mods

ADD ./deploy /code
ADD ./db /db
RUN chown -R root:devilbox /code \
    && chmod -R 440 /code \
    && chmod 550 /code
RUN chown -R root:devilbox /db \
    && chmod -R 440 /db \
    && chmod 550 /db
