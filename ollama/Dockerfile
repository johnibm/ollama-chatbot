FROM docker.io/ollama/ollama:latest

# Become root to set up the environment
USER 0

# Copy and prepare startup script
COPY startup.sh /startup.sh
RUN chmod g+rx /startup.sh && chown 1001:0 /startup.sh

# Drop to non-root user (compatible with OpenShift)
USER 1001

# Entrypoint
ENTRYPOINT ["/startup.sh"]