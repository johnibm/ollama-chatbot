# ollama-streamlit


## Intructions

## Openshift
### Create Project
oc new-project ollama-streamlit

### Create Ollama Deployment
oc apply -f deployments/ollama.yaml
#### Or with GPU support
oc apply -f deployments/ollama-gpu.yaml

### Create Chatbot Deployment
oc apply -f deployments/chatbot.yaml



