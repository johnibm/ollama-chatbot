FROM docker.io/ollama/ollama:latest

# Become root to set up the environment
USER 0

# Set permissions on the working directory (so any UID can write)
RUN chgrp -R 0 . && chmod -R g+rwX .

# Add startup script
COPY startup.sh /startup.sh

# Ensure the current directory is executable and writable by the root group
RUN chown 0:0 . && chmod g+rx .

# Ensure the script is executable and writable by the root group
RUN chown 0:0 /startup.sh && chmod g+rx /startup.sh

# Drop to a random OpenShift-assigned user (1001+)
USER 1001

# Entrypoint
ENTRYPOINT ["/startup.sh"]
