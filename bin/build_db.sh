#!/usr/bin/env bash
DB_NAME='DaftScraper'

echo 'Installing mysql-server'
sudo apt-get install -yqq mysql-server

echo "Creating $DB_NAME Database"
mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

echo '    Importing schema'
mysql -uroot -p $DB_NAME < DaftScraper/schemas.sql
