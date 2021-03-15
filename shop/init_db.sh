#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE DATABASE rl_shop;
    CREATE USER shop_slave WITH PASSWORD 'shop';
    GRANT ALL PRIVILEGES ON DATABASE "rl_shop" to shop_slave;
EOSQL