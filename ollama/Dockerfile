FROM docker.io/ollama/ollama:latest

# Become root to set up the environment
USER 0

# Add startup script
COPY startup.sh /startup.sh
# Ensure the script is executable and writable by the root group
RUN chown 0:0 /startup.sh && chmod g+rx /startup.sh

# Drop to a random OpenShift-assigned user (1001+)
USER 1001

# Entrypoint
ENTRYPOINT ["/startup.sh"]
