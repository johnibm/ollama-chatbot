FROM docker.io/ollama/ollama:latest
USER 0
RUN chgrp -R 0 . && chmod -R g+rwX .  
COPY startup.sh /startup.sh
RUN chown -R 1001:0 ./
RUN chmod +x /startup.sh
USER 1001
ENTRYPOINT ["/startup.sh"]
