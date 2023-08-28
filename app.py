import streamlit as st
import json
import uuid

from medisearch_client import MediSearchClient

api_key = "gx4XXBhE7Zrga682gmEm"
conversation_id = str(uuid.uuid4())
client = MediSearchClient(api_key=api_key)

# 初始化聊天历史
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 标题图
# st.title('AiDoctor')
st.set_page_config(page_title='AiDoctor')

st.image("deer.png", use_column_width=True)
    
# 输入问题聊天框
user_input = st.text_area("\n\n", placeholder='请输入您想了解的医疗问题')
# text = st.text_area('请输入文本', height=3)

# checkbox_state = st.checkbox("清除历史数据")

# if checkbox_state == True:
#     st.session_state.chat_history = []

# st.markdown("\n\n常见问题(AI意见仅供参考，请只从医学专业人士那里获取建议):")
styled_text = f"<span style='color: #FF7F50;'>常见问题:</span>"
st.markdown(styled_text, unsafe_allow_html=True)

st.markdown("- 对于感冒症状，有哪些理疗方法可以缓解鼻塞和喉咙痛？")
st.markdown("- 鼻炎患者在理疗过程中，有没有什么特别的注意事项或推荐的治疗方法？")
st.markdown("- 如何通过理疗来加速运动损伤的康复过程？有哪些常用的理疗方法可以减轻疼痛和促进恢复？")
    
# 提交按钮
text_response = ''
is_empty = False

submit_button = st.button("提问")

if submit_button:
    with st.spinner('正在分析输出...'):
        if not user_input:
            is_empty = True
            st.error("请填写问题后再提交")
        else:
            # 历史消息
            checkbox_state = False
            historylen = len(st.session_state.chat_history)
            
            if historylen > 0: 
                
                responses = client.send_user_message(conversation=[st.session_state.chat_history[historylen-1]['user'],
                                                           st.session_state.chat_history[historylen-1]['ai_doctor'],
                                                           user_input],
                                             conversation_id=conversation_id,
                                             language="Chinese",
                                             should_stream_response=True)
            # 新消息
            else:
                
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
    
            st.write(st.session_state.chat_history)
            st.write(conversation_id)
            
            for index, articles in enumerate(text_url_response):
                st.markdown(f"[{index+1}] {articles['title']} {articles['url']}")
    
            # 更新聊天历史
            if len(text_url_response) > 0:
                st.session_state.chat_history.append({
                    'user': user_input,
                    'ai_doctor': text_response
                })
            
            # print(chat_history)

if is_empty:
    submit_button = False

# 模型说明
st.markdown("""
### More details
:fire: iDoctor has a performance of`92%`on the United States medical licensing sample exam (USMLE).The 2022 USMLE sample benchmark was first used to evaluate the medical question answering ability of :robot: ChatGPT. We obtained other systems' performances (OpenEvidence, GPT4) from their associated papers and reports.
""")

# 隐藏
hide_streamlit_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_streamlit_style = """<style>.stApp [data-testid="stToolbar"]{ display:none;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
