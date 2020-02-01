FROM php:7.1-fpm

RUN apt-get update --fix-missing
RUN apt-get install -y curl
RUN apt-get install -y build-essential libssl-dev zlib1g-dev libpng-dev libjpeg-dev libfreetype6-dev

RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd

ADD ./deploy /code
RUN chown -R root:www-data /code \
    && chmod -R 440 /code \
    && chmod 550 /code
