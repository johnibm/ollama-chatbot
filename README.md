# ollama-chatbot


## Intructions for Openshift
### Create Project
oc new-project demo-ollama-chatbot

### Create Ollama Deployment
oc apply -f deployments/ollama-gpu.yaml

### Create Chatbot Deployment
oc apply -f deployments/chatbot.yaml



