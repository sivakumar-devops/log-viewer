FROM php:8.2-apache

# Install dependencies
RUN apt-get update && \
    apt-get install -y libsqlite3-dev && \
    docker-php-ext-install pdo pdo_sqlite

# Install Python (Debian/Ubuntu)
RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*

# Enable Apache rewrite
RUN a2enmod rewrite

# Copy app source
COPY . /var/www/html

# set working dir
WORKDIR /var/www/html

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install PHP dependencies
RUN composer install --optimize-autoloader --no-dev

# Publish Log Viewer assets
RUN php artisan vendor:publish --tag=log-viewer-assets --force
# Copy apache conf file
COPY ./vhost.conf /etc/apache2/sites-available/000-default.conf
# Copy log viewer file
COPY docker/log-viewer.php /var/www/html/config/log-viewer.php
# Copy log viewer file
COPY docker/consolidate_logs.py /var/www/html/consolidate_logs.py 
# Add custom entrypoint
COPY docker/entrypoint.sh /var/www/html/docker/entrypoint.sh
RUN chmod +x /var/www/html/docker/entrypoint.sh

EXPOSE 80
