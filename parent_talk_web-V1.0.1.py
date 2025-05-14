import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(layout="wide", page_title="角色扮演式育兒語氣轉換器", page_icon="🧸")

# 高級感活潑動畫背景（使用純CSS動畫，避免SVG造成空白）
st.markdown(
    """
<style>
body, .stApp {
    background: linear-gradient(120deg, #ffe6e6 0%, #fffbe6 40%, #e6f7ff 80%, #ffe6fa 100%) !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}
.animated-bg-bubble {
    position: fixed;
    z-index: 0;
    border-radius: 50%;
    opacity: 0.35;
    filter: blur(2px);
    animation: floatbubble 12s ease-in-out infinite alternate;
}
.bubble1 {
    width: 320px; height: 320px; left: 5vw; top: 8vh; background: #ffe6e6; animation-delay: 0s;
}
.bubble2 {
    width: 400px; height: 400px; right: 8vw; top: 60vh; background: #e6f7ff; animation-delay: 2s;
}
.bubble3 {
    width: 220px; height: 220px; left: 40vw; top: 40vh; background: #fffbe6; animation-delay: 4s;
}
@keyframes floatbubble {
    0%% { transform: translateY(0) scale(1); }
    100%% { transform: translateY(-40px) scale(1.08); }
}
.block-container { padding-top: 2rem; position: relative; z-index: 1; }
.apple-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #ff5a36;
    letter-spacing: -1px;
    margin-bottom: 0.5em;
    font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    text-shadow: 0 2px 8px #fffbe6cc;
    z-index: 2;
}
.apple-card {
    background: linear-gradient(135deg, #fff 60%, #ffe6fa 100%);
    border-radius: 22px;
    box-shadow: 0 6px 32px 0 #ffbfa340, 0 1.5px 6px 0 #6ec6ff30;
    border: 1.5px solid #ffe6e6;
    color: #222 !important;
    padding: 1.5em 1.5em 1em 1.5em;
    margin-bottom: 1.5em;
    animation: popin 0.7s cubic-bezier(.68,-0.55,.27,1.55);
    position: relative;
    z-index: 2;
}
@keyframes popin {
    0%% { transform: scale(0.8); opacity: 0; }
    100%% { transform: scale(1); opacity: 1; }
}
/* 強制 Streamlit 轉換按鈕為彩色動態漸層 */
button[kind="primary"], .stForm button, .stButton > button {
    background: linear-gradient(270deg, #ffb347, #ff7f50, #6ec6ff, #ffb347) !important;
    background-size: 600% 600% !important;
    animation: livelybtn 3s ease-in-out infinite !important;
    color: #fff !important;
    border-radius: 18px !important;
    font-size: 1.25rem !important;
    font-weight: 700;
    padding: 0.7em 2.2em !important;
    box-shadow: 0 4px 16px 0 #ffbfa380, 0 1.5px 6px 0 #ff7f5030;
    border: none !important;
    transition: background 0.3s, box-shadow 0.3s;
}
@keyframes livelybtn {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
button[kind="primary"]:hover, .stForm button:hover, .stButton > button:hover {
    filter: brightness(1.08) saturate(1.2);
    box-shadow: 0 6px 24px 0 #ffbfa3cc;
}
.apple-btn > button, .stForm button[kind='primary'] {
    background: linear-gradient(270deg, #ffb347, #ff7f50, #6ec6ff, #ffb347) !important;
    background-size: 600% 600% !important;
    animation: livelybtn 3s ease-in-out infinite;
    color: #fff !important;
    border-radius: 18px !important;
    font-size: 1.25rem !important;
    font-weight: 700;
    padding: 0.7em 2.2em !important;
    box-shadow: 0 4px 16px 0 #ffbfa380, 0 1.5px 6px 0 #ff7f5030;
    border: none !important;
    transition: background 0.3s, box-shadow 0.3s;
}
.apple-btn > button:hover, .stForm button[kind='primary']:hover {
    filter: brightness(1.08) saturate(1.2);
    box-shadow: 0 6px 24px 0 #ffbfa3cc;
}
.apple-chat-user { color: #ff7f50; font-weight: 700; }
.apple-chat-ai { color: #0071e3; font-weight: 600; }
.apple-chat-time { color: #888; font-size: 0.95em; margin-left: 0.5em; }
.apple-divider { border-top: 1px solid #e0e0e0; margin: 0.5em 0 1em 0; }
.fullwidth { width: 100% !important; }
.stTextArea textarea {
    background: #fff !important;
    border-radius: 14px !important;
    border: 2px solid #ffbfa3 !important;
    color: #222 !important;
    font-size: 1.15rem !important;
    box-shadow: 0 2px 8px 0 #ffe6e680;
    transition: box-shadow 0.3s;
    caret-color: #111 !important;
}
.stTextArea textarea:focus {
    box-shadow: 0 4px 16px 0 #ff7f5040;
    border: 2px solid #ff7f50 !important;
}
.stTextArea textarea::placeholder {
    color: rgba(120,120,120,0.45) !important;
    font-size: 1.08rem !important;
    font-style: italic;
    letter-spacing: 0.5px;
}
.stTextArea label, label[for^='input_area'] {
    color: #111 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.5px;
}
.stSpinner > div > div {
    color: #222 !important;
    font-weight: 700;
    font-size: 1.15rem;
    display: flex;
    align-items: center;
    gap: 0.5em;
}
.stSpinner > div > div:before {
    content: '';
    display: inline-block;
    width: 32px;
    height: 32px;
    background-image: url('https://cdn.jsdelivr.net/gh/innocces/animal-gif@main/running-cat.gif');
    background-size: contain;
    background-repeat: no-repeat;
    margin-right: 0.5em;
    vertical-align: middle;
    animation: animalrun 1.2s linear infinite;
}
@keyframes animalrun {
    0% { transform: translateX(0); }
    50% { transform: translateX(16px); }
    100% { transform: translateX(0); }
}
</style>
<div class="animated-bg-bubble bubble1"></div>
<div class="animated-bg-bubble bubble2"></div>
<div class="animated-bg-bubble bubble3"></div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="apple-title">🧸 遊戲化親子語言轉換器</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:1.15rem; color:#444; margin-bottom:1.5em; background:rgba(255,255,255,0.7); border-radius:14px; padding:1em 1.5em; box-shadow:0 2px 8px #0001;">這是一款專為家長設計的「遊戲化親子語言轉換器」。<br>只要輸入你想和孩子說的話，系統會自動將其轉換成更有趣、角色扮演、遊戲化、正向鼓勵等風格的親子語言，讓日常溝通變得更有創意與溫度！</div>', unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state['history'] = []

col1, col2 = st.columns([1, 1])

with col1:
    with st.form("parent_talk_form", clear_on_submit=False):
        user_input = st.text_area(
            "請輸入你想和孩子說的話",
            height=100,
            key="input_area",
            placeholder="例如：快去刷牙、吃飯囉、該睡覺了……",
            help="按 Enter 送出，Shift+Enter 換行",
            label_visibility="visible"
        )
        submitted = st.form_submit_button("轉換", use_container_width=True)
    st.markdown("<div class='apple-divider'></div>", unsafe_allow_html=True)
    if submitted and user_input.strip():
        with st.spinner("轉換中..."):
            prompt = f"""
請將下列語句隨機選擇一種「遊戲化親子語言」風格（包含但不限於：擬人化／角色扮演、遊戲化、正向鼓勵、畫面感、溫柔幽默），並直接轉換成有創意且符合該風格的語句，不要加任何說明或客套話：
{user_input}
"""
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-DmKceRwr6AUlf04z0a58BaE4B5Bf46Ad806aC898D1Be0915"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "你是專業的親子語言轉換助手。"},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post("https://free.v36.cm/v1/chat/completions", headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"].strip()
                st.session_state['history'].append({
                    'user': user_input,
                    'ai': result,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                st.markdown(f"<div class='apple-card'><span class='apple-chat-ai'>{result}</span></div>", unsafe_allow_html=True)
            else:
                st.error("API 請求失敗，請稍後再試。")

with col2:
    st.markdown("<div class='apple-card'><b>對話紀錄</b></div>", unsafe_allow_html=True)
    for item in reversed(st.session_state['history']):
        st.markdown(f"""
        <div class='apple-card' style='position:relative;'>
            <span class='apple-chat-time' style='position:absolute; top:1em; right:1.5em;'>{item['time']}</span>
            <span class='apple-chat-user'>你：</span> {item['user']}<br>
            <span class='apple-chat-ai'>AI：</span> {item['ai']}
        </div>
        """, unsafe_allow_html=True)