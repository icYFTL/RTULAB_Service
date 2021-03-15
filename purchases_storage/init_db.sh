#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE DATABASE rl_purchases;
    CREATE USER purchases_slave WITH PASSWORD 'purchases';
    GRANT ALL PRIVILEGES ON DATABASE "rl_purchases" to purchases_slave;
EOSQL