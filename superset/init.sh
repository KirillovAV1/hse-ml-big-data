#!/usr/bin/env bash
set -e

superset db upgrade

superset fab create-admin \
  --username "${SUPERSET_ADMIN_USERNAME}" \
  --firstname "${SUPERSET_ADMIN_FIRST_NAME}" \
  --lastname "${SUPERSET_ADMIN_LAST_NAME}" \
  --email "${SUPERSET_ADMIN_EMAIL}" \
  --password "${SUPERSET_ADMIN_PASSWORD}" || true

superset fab reset-password \
  --username "${SUPERSET_ADMIN_USERNAME}" \
  --password "${SUPERSET_ADMIN_PASSWORD}" 

superset init
superset run -h 0.0.0.0 -p 8088
