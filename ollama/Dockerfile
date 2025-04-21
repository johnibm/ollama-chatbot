FROM docker.io/ollama/ollama:latest
USER 0

COPY startup.sh /startup.sh
RUN chgrp -R 0 . && chmod -R g+rwX .  
RUN chown -R 1001:0 ./
RUN chmod +x /startup.sh
USER 1001
ENTRYPOINT ["/startup.sh"]
