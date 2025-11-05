#!/usr/bin/env bash

set -e

echo "Run apply migrations.."
alembic upgrade e032f2b2bb3d
echo "Migrations applied!"

exec "$@"