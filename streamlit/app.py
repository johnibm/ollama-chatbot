# https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/
import os
import streamlit as st
from PIL import Image


from llama_index.core import ServiceContext, Document, SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
print(f"Connecting to ollama server {OLLAMA_HOST}")

# Use zephyr:latest directly
my_llm = "zephyr:latest"  # Model name: zephyr

ollama_llm = Ollama(model=my_llm, base_url="http://" + OLLAMA_HOST + ":11434")
Settings.llm = ollama_llm
ollama_embedding = OllamaEmbedding(
    model_name="mxbai-embed-large",
    base_url="http://"+OLLAMA_HOST+":11434",
    ollama_additional_kwargs={"mirostat": 0},
)

system_prompt = \
    "You are Chatbot, an expert on Memorial University of Newfoundland, located in St John's, Newfoundland, Canada. Your job is to answer questions about Memorial University and Newfoundland. " \
    "Assume that all questions are related to Memorial Universty and/or the province of Newfoundland in Canada. " \
    "Keep your answers to a few sentences and based on context - do not hallucinate facts. " \
    "Output markdown and always try to cite your source document. "

st.set_page_config(page_title="MUN Chatbot 🤖", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

# Display custom logo image
logo = Image.open('./images/MUN_Logo_CMYK_color.jpg')  # Open image file
logo = logo.resize((105, 62)) 
#st.image(logo, width=None)  # Display the image with default width
st.image(logo) 

st.title("MUN Chatbot 🤖")
#st.subheader("Everything you want to know about the Memorial University of Newfoundland")
st.markdown(
    '<h4 style="white-space: nowrap;">Everything you want to know about the Memorial University of Newfoundland</h4>',
    unsafe_allow_html=True
)

with st.sidebar.expander("Settings"):
    system_prompt = st.text_area('System Prompt', value=system_prompt, height=256)
    #my_llm = st.text_area('Model', value=my_llm)
    my_llm = st.selectbox("Model", options=["llama3:8b", "gemma:2b", "mistral:7b-instruct-v0.3-q8_0", "zephyr"], index=0)

if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Memorial University"}
    ]

@st.cache_resource(show_spinner=False)
def load_data(_llm):
    with st.spinner(text="Loading and indexing the document data – might take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        
        Settings.llm = ollama_llm
        Settings.embed_model = ollama_embedding
        index = VectorStoreIndex.from_documents(docs)

        return index


index = load_data(ollama_llm)

chat_engine = index.as_chat_engine(
    chat_mode="simple", verbose=True, system_prompt=system_prompt
)

if prompt := st.chat_input("Ask me a question about Memorial University"): 
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Querying..."):
            streaming_response = chat_engine.stream_chat(prompt)
            placeholder = st.empty()
            full_response = ''
            for token in streaming_response.response_gen:
                full_response += token
                placeholder.markdown(full_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })
