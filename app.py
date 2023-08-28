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

# 显示聊天历史
for chat in chat_history:
    st.text(chat['user'])
    st.text(chat['ai_doctor'])
    st.markdown(f"答案出处: [{chat['title']}]({chat['url']})")

# 输入问题聊天框
user_input = st.text_input("请输入您的问题：")

# 提交按钮
if st.button("提问"):
    # # AI医生的回答（模拟）
    # ai_answer = "这是AI医生的回答。"
    # source_url = "https://example.com/source"
    
    responses = client.send_user_message(conversation=[user_input],
                                     conversation_id=conversation_id,
                                     language="Chinese",
                                     should_stream_response=False)

    for response in responses:
      if response["event"] == "llm_response":
        text_response = response["text"]
      if response["event"] == "articles":
        text_url_response = response["articles"] 


    # 更新聊天历史
    chat_history.append({
        'user': f"用户: {user_input}",
        'ai_doctor': f"AI医生: {text_response}",
        'source': text_url_response
    })

print(chat_history)

# 三个参考问题
st.write('常见问题')
st.markdown("- 对于感冒症状，有哪些理疗方法可以缓解鼻塞和喉咙痛？")
st.markdown("- 鼻炎患者在理疗过程中，有没有什么特别的注意事项或推荐的治疗方法？")
st.markdown("- 如何通过理疗来加速运动损伤的康复过程？有哪些常用的理疗方法可以减轻疼痛和促进恢复？")
