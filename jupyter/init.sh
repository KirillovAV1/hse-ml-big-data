#!/bin/bash
set -e

if ! id "$JUPYTER_USER"; then
    useradd -m -s /bin/bash "$JUPYTER_USER"
fi

echo "$JUPYTER_USER:$JUPYTER_PASSWORD" | chpasswd

mkdir -p "/home/$JUPYTER_USER/.local/share/jupyter/runtime"
mkdir -p "/home/$JUPYTER_USER/work"

chown -R "$JUPYTER_USER:$JUPYTER_USER" "/home/$JUPYTER_USER"

exec jupyterhub -f /jupyterhub_config.py