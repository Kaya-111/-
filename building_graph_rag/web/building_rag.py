import time
import base64
import requests
import streamlit as st

from model_config import model_config

def building_rag_agent():
    st.markdown(
        """
        <style>
        .centered-title {
            text-align: center;
            font-size: 2em;
            color: #27AE60;  /* 设置字体颜色，例如橙红色 */
        }
        </style>
        <h1 class="centered-title">论文问答界面</h1>
        """,
        unsafe_allow_html=True
    )

    model_selection = st.sidebar.selectbox(label="model_selection", 
                            options=["DeepSeek R1", "DeepSeek V3"])

    embedding_selection = st.sidebar.selectbox(label="embedding_selection", 
                            options=["m3e-base", "m3e-large", "bge-small-zh", "bge-base-zh", "bge-large-zh"])

    temperature = st.sidebar.slider('大模型温度系数', min_value=0.0, max_value=1.0, value=0.95, step=0.1)
    if temperature == 0.0:
        temperature = 0.1

    def control_sidebar_button_poisition(num):
        for _ in range(num):
            st.sidebar.write("\n")

    control_sidebar_button_poisition(3)

    def sidebar_bg(side_bg):
        side_bg_ext = 'png'
        
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] > div:first-child {{
                background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
            }}
            </style>
            """,
            unsafe_allow_html=True,
            )

    #sidebar_bg("images/sidebar_bg4.jpg")

    # 添加侧边栏按钮，用于清空对话
    if st.sidebar.button("clear"):
        st.session_state.check_messages = []

    # Initialize chat history
    if "check_messages" not in st.session_state:
        st.session_state.check_messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.check_messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="images/kefu1.jpg"):
                st.markdown(message["content"])
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="images/kefu2.jpg"):
                st.markdown(message["content"])

    # React to user input
    if query := st.chat_input("your question"):
        # Display user message in chat message container
        st.chat_message("user", avatar="images/kefu1.jpg").markdown(query)
        # Add user message to chat history
        st.session_state.check_messages.append({"role": "user", "content": query})

        # 请求API
        API_URL = model_config.API_URL

        # RAG语料召回
        #recall_chunks = index_db.similarity_search(query)
        rag_recall = requests.post(
            f"{API_URL}/rag_retrieval", json={"query": query}
        )
        if rag_recall.status_code == 200:
            content = rag_recall.json()
            rag_chunks = content["content"]
        else:
            rag_chunks = ""
        # Graph语料召回
        graph_recall = requests.post(
            f"{API_URL}/graph_retrieval", json={"query": query}
        )
        if graph_recall.status_code == 200:
            content = graph_recall.json()
            graph_chunks = content["content"]
        else:
            graph_chunks = ""

        response = requests.post(
            f"{API_URL}/rag_chat", json={"query": query, "rag_chunks": rag_chunks, \
                                               "graph_chunks": graph_chunks, "temperature": temperature}
        )
        if response.status_code == 200:
            content = response.json()
            rag_response = content["content"]
        # 在chat message container中显示助手消息
        with st.chat_message("assistant", avatar="images/kefu2.jpg"):
            # 模拟逐字输出效果
            response_placeholder = st.empty()
            typed_text = ""
            for char in rag_response:
                typed_text += char
                response_placeholder.markdown(f"**Answer**： {typed_text.replace('  ', '  <br>')}", unsafe_allow_html=True)
                time.sleep(0.05)  # 控制输出速度
            #response = st.write_stream(response_generator_compare(rag_response, "llm+rag"))
        # 消息记录到历史记录里面
        st.session_state.check_messages.append({"role": "assistant", "content": rag_response})