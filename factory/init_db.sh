#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE DATABASE rl_factory;
    CREATE USER factory_slave WITH PASSWORD 'factory';
    GRANT ALL PRIVILEGES ON DATABASE "rl_factory" to factory_slave;
EOSQL