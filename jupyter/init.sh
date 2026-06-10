#!/bin/bash
set -e

if ! id "$JUPYTER_USER"; then
    useradd -m -s /bin/bash "$JUPYTER_USER"
fi

echo "$JUPYTER_USER:$JUPYTER_PASSWORD" | chpasswd

exec jupyterhub --Authenticator.allow_all=True