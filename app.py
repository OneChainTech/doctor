import streamlit as st
import json
import uuid

from medisearch_client import MediSearchClient

api_key = "gx4XXBhE7Zrga682gmEm"
conversation_id = str(uuid.uuid4())
client = MediSearchClient(api_key=api_key)

# 初始化聊天历史
chat_history = []

# 标题图
st.image("deer.png", use_column_width=True)

# st.markdown("\n\n常见问题(AI意见仅供参考，请只从医学专业人士那里获取建议):")
styled_text = f"<span style='color: #FF7F50;'>常见问题:</span>"
st.markdown(styled_text, unsafe_allow_html=True)

st.markdown("- 对于感冒症状，有哪些理疗方法可以缓解鼻塞和喉咙痛？")
st.markdown("- 鼻炎患者在理疗过程中，有没有什么特别的注意事项或推荐的治疗方法？")
st.markdown("- 如何通过理疗来加速运动损伤的康复过程？有哪些常用的理疗方法可以减轻疼痛和促进恢复？")

# 输入问题聊天框
user_input = st.text_area("\n\n", placeholder='请输入您的问题')
# text = st.text_area('请输入文本', height=3)

# 提交按钮
if st.button("提问"):
    
    responses = client.send_user_message(conversation=[user_input],
                                     conversation_id=conversation_id,
                                     language="Chinese",
                                     should_stream_response=True)
    
    output_container = st.empty()
    
    for response in responses:
      if response["event"] == "llm_response":
        text_response = response["text"]
        output_container.write(f'{text_response}')
      if response["event"] == "articles":
        text_url_response = response["articles"] 

    # 更新聊天历史
    chat_history.append({
        'user': {user_input},
        'ai_doctor': {text_response}
    })

    for index, articles in enumerate(text_url_response):
        st.markdown(f"[{index+1}] {articles['title']} {articles['url']}")

    print(chat_history)


# 模型说明
st.markdown("""
### More details
:fire: AiDoctor has a performance of `92% ` on the United States medical licensing sample exam 
(USMLE, https://www.usmle.org/, dataset). You can find the answers that AiDoctor produced here: 
USMLE Step 1, USMLE Step 2, USMLE Step 3. To the best of our knowledge, this is the highest performance 
out of any question-answering system evaluated on the USMLE sample exam. 
""")
st.markdown("""If you have any questions,please :mailbox: Mail to zhenghong596gm@gmail.com""")

# 隐藏
hide_streamlit_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_streamlit_style = """<style>.stApp [data-testid="stToolbar"]{ display:none;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
