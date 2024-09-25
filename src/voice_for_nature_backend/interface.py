import streamlit as st
from interface_utils import save_file, FILES_DIR
from voice_for_nature_backend.chat_model import setup_llm, get_data, create_index

CACHE_DIR = r"C:\MyComputer\llm\models"
setup_llm(cache_dir=CACHE_DIR)
documents = get_data()
index = create_index(documents)
query_engine = index.as_query_engine()

st.title("Echo Chat")

with st.sidebar:
    # inputs and parameters in the sidebar
    max_new_tokens = st.number_input("max_new_tokens", 128, 4096, 512)
    k = st.number_input("k", 1, 10, 3)
    uploaded_files = st.file_uploader(
        "Upload PDFs for context", type=["PDF", "pdf"], accept_multiple_files=True
    )
    file_paths = []
    for uploaded_file in uploaded_files:
        file_paths.append(save_file(uploaded_file))

    if uploaded_files:
        documents = get_data(FILES_DIR)
        index = create_index(documents)
        query_engine = index.as_query_engine()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message): #["role"]
#         st.markdown(message) # ["content"]

# Accept user input
if prompt := st.chat_input("Ask me anything!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display Echo Chat response in chat message container
    with st.chat_message("Nature voice"):
        user_prompt = st.session_state.messages[-1]["content"]
        answer = query_engine.query(user_prompt)

        st.write({f"Eco chat:{answer.response}"})
        # answer = response
        reference_id = [
            answer.metadata[key]["file_name"] for key in answer.metadata.keys()
        ]
        reference_text = [
            answer.source_nodes[i].text for i in range(len(answer.source_nodes))
        ]
        score = [answer.source_nodes[i].score for i in range(len(answer.source_nodes))]

        references = {
            f"{key}({round(score_i, 2)})": value
            for key, score_i, value in zip(reference_id, score, reference_text)
        }
        for key, value in references.items():
            st.write(f"{key}: {value}")
        # st.write(f"References: {references}")
    st.session_state.messages.append(answer.response)
