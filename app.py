import streamlit as st

# 初始化聊天历史
chat_history = []

# 标题图
st.image("deer.png", caption="deer", use_column_width=True)

# 聊天对话界面
st.title("AI医生与用户聊天界面")

# 显示聊天历史
for chat in chat_history:
    st.text(chat['user'])
    st.text(chat['ai_doctor'])
    st.markdown(f"答案出处: [{chat['source']}]({chat['source']})")

# 输入问题聊天框
user_input = st.text_input("请输入您的问题：")

# 提交按钮
if st.button("提交"):
    # AI医生的回答（模拟）
    ai_answer = "这是AI医生的回答。"
    source_url = "https://example.com/source"

    # 更新聊天历史
    chat_history.append({
        'user': f"用户: {user_input}",
        'ai_doctor': f"AI医生: {ai_answer}",
        'source': source_url
    })

# 三个参考问题
st.title("参考问题")
st.markdown("1. [关于感冒的问题案例](https://example.com/cold)")
st.markdown("2. [关于鼻炎的问题案例](https://example.com/rhinitis)")
st.markdown("3. [关于运动损伤的问题案例](https://example.com/sports_injury)")
