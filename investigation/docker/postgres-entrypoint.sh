#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE activities;
	CREATE TABLE IF NOT EXISTS reviews(
	  user_id VARCHAR(100),
	  film_id VARCHAR(100),
	  text VARCHAR(1000)
	);
EOSQL