#!/bin/bash
set -e

echo "📌 Running custom Laravel Entrypoint"

APP_DIR=/var/www/html

echo "✅ Fixing permissions on storage and bootstrap/cache..."
chown -R www-data:www-data $APP_DIR/storage $APP_DIR/bootstrap/cache
chmod -R 775 $APP_DIR/storage $APP_DIR/bootstrap/cache

echo "✅ Checking for SQLite cache files..."
find $APP_DIR/storage -name "*.sqlite" -exec chmod 664 {} \;

echo "✅ Running Artisan commands..."
cd $APP_DIR
php artisan config:clear || echo "⚠️ Could not clear config cache (probably not yet set up)"
php artisan cache:clear || echo "⚠️ Could not clear app cache (probably not yet set up)"
php artisan view:clear || echo "⚠️ Could not clear views cache (probably not yet set up)"

# Ensure database directory is writable
echo "✅ Fixing permissions for SQLite..."
mkdir -p database
chown -R www-data:www-data database
chmod -R 775 database

# Ensure database exists
if [ ! -f database/database.sqlite ]; then
  echo "✅ Creating SQLite database..."
  touch database/database.sqlite
fi

chmod 664 database/database.sqlite
chown www-data:www-data database/database.sqlite

# Ensure cache table exists
php artisan cache:table || echo "⚠️ Cache table may already exist"

# Run migrations
php artisan migrate --force || echo "⚠️ Migrations may already be up to date"

echo "✅ Running Python log consolidation..."
python3 ./consolidate_logs.py || echo "⚠️ Log consolidation failed"

echo "✅ Entrypoint completed. Starting Apache..."
exec apache2-foreground
