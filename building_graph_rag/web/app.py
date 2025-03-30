import streamlit as st
#import streamlit_authenticator as stauth

from building_rag import building_rag_agent

st.set_page_config(
    page_title='rag应用平台',
    layout='wide')


# 创建一个字典来存储页面名称和对应的函数
pages = {
    "建筑文章生成助手": building_rag_agent,
}

# 使用 sidebar 选择页面
st.sidebar.title("AI智能应用平台")
selection = st.sidebar.radio("功能选择", list(pages.keys()))

pages[selection]()

