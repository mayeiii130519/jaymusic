import streamlit as st
import random
import openai
import os
from dotenv import load_dotenv

# --- 初始化 ---
st.set_page_config(page_title="AI JAYBOX", page_icon="🎧")
st.title("🎧 AI JAYBOX")

# --- 載入 OpenAI 金鑰 ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- 使用者輸入區塊 ---
st.write("請輸入你目前的狀況或心情，我們會為你推薦一首周杰倫的歌：")
st.caption("舉例：我剛分手了 / 今天考試壓力好大 / 剛剛和朋友吃飯覺得很幸福")
user_input = st.text_area("📝 請輸入你的心情或發生的事情")
method = st.selectbox("🔍 選擇情緒判斷方式", ["使用 GPT 模型（推薦）", "使用內建規則法"])

# --- 周杰倫歌曲資料庫 ---
emotion_song_map = {
    "開心": [
        {"title": "晴天", "youtube": "https://www.youtube.com/watch?v=DYptgVvkVLQ", "lyrics": "故事的小黃花，從出生那年就飄著..."},
        {"title": "甜甜的", "youtube": "https://www.youtube.com/watch?v=mm8T-lBXQXA", "lyrics": "你突然對我說，baby 我好想你..."},
        {"title": "可愛女人", "youtube": "https://www.youtube.com/watch?v=87VUC4J_0Ps", "lyrics": "想要有直升機，想要和你飛到宇宙去..."},
    ],
    "傷心": [
        {"title": "安靜", "youtube": "https://www.youtube.com/watch?v=1hI-7vj2FhE", "lyrics": "只剩下鋼琴陪我彈了一天..."},
        {"title": "退後", "youtube": "https://www.youtube.com/watch?v=0-4mm0e2h44", "lyrics": "我們的愛 過了就不再回來..."},
        {"title": "說好的幸福呢", "youtube": "https://www.youtube.com/watch?v=mLFhTFiX0uM", "lyrics": "你的回話 凌亂著..."},
    ],
    "平淡": [
        {"title": "蒲公英的約定", "youtube": "https://www.youtube.com/watch?v=VitJnr3IySc", "lyrics": "陪我走過那森林..."},
        {"title": "好久不見", "youtube": "https://www.youtube.com/watch?v=uAUBexRRFr0", "lyrics": "我來到 你的城市..."},
        {"title": "稻香", "youtube": "https://www.youtube.com/watch?v=sHD_z90ZKV0", "lyrics": "對這個世界如果你有太多的抱怨..."},
    ],
    "戀愛": [
        {"title": "告白氣球", "youtube": "https://www.youtube.com/watch?v=bu7nU9Mhpyo", "lyrics": "親愛的愛上你，從那天起..."},
        {"title": "簡單愛", "youtube": "https://www.youtube.com/watch?v=Y4xCVlyCvX4", "lyrics": "我想就這樣牽著你的手..."},
        {"title": "浪漫手機", "youtube": "https://www.youtube.com/watch?v=Kbvu9Vt5_eE", "lyrics": "你的訊息總是讓我心跳加速..."},
    ],
    "生氣": [
        {"title": "以父之名", "youtube": "https://www.youtube.com/watch?v=9q7JOQfcJQM", "lyrics": "在以父之名之下..."},
        {"title": "四面楚歌", "youtube": "https://www.youtube.com/watch?v=JljURsMOLmc", "lyrics": "我站在台上講話你卻在睡覺..."},
        {"title": "雙截棍", "youtube": "https://www.youtube.com/watch?v=OR-0wptI_u0", "lyrics": "快使用雙截棍..."},
    ],
    "焦慮": [
        {"title": "夜的第七章", "youtube": "https://www.youtube.com/watch?v=AdkkF6MT0R0", "lyrics": "黑夜的第七章..."},
        {"title": "止戰之殤", "youtube": "https://www.youtube.com/watch?v=qIZ5MAwbeCg", "lyrics": "鮮血染紅了鴿子的翅膀..."},
        {"title": "黑色幽默", "youtube": "https://www.youtube.com/watch?v=wRT-5heURhY", "lyrics": "敗給你的黑色幽默..."},
    ],
    "孤單": [
        {"title": "擱淺", "youtube": "https://www.youtube.com/watch?v=YJfHuATJYsQ", "lyrics": "那種感覺像擱淺..."},
        {"title": "說了再見", "youtube": "https://www.youtube.com/watch?v=KKsioz-zaZY", "lyrics": "說了再見，才發現再也見不到你..."},
        {"title": "夜曲", "youtube": "https://www.youtube.com/watch?v=6Q0Pd53mojY", "lyrics": "黑色的夜悄悄落下..."},
    ]
}

# --- GPT 情緒判斷 ---
def gpt_emotion_classifier(text):
    prompt = f"""你是一位情緒分析專家，請根據以下使用者描述判斷其當前心情狀態。
請你只回覆以下七個類別之一：開心、傷心、平淡、戀愛、生氣、焦慮、孤單。
不要解釋，不要加任何標點，只輸出一個詞。
使用者輸入：「{text}」
你判斷的情緒是："""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=10
        )
        emotion = response.choices[0].message['content'].strip()
        return emotion if emotion in emotion_song_map else rule_based_emotion_classifier(text)
    except:
        return rule_based_emotion_classifier(text)

# --- 簡化版規則法 ---
def rule_based_emotion_classifier(text):
    text = text.lower()
    if any(word in text for word in ["愛", "喜歡", "戀愛", "幸福"]):
        return "戀愛"
    elif any(word in text for word in ["考試", "壓力", "焦慮", "煩"]):
        return "焦慮"
    elif any(word in text for word in ["吵架", "生氣", "討厭", "氣死"]):
        return "生氣"
    elif any(word in text for word in ["孤單", "寂寞", "一個人"]):
        return "孤單"
    elif any(word in text for word in ["哭", "低落", "分手", "傷心"]):
        return "傷心"
    elif any(word in text for word in ["開心", "快樂", "高興"]):
        return "開心"
    else:
        return "平淡"

# --- 建議語句生成 ---
def gpt_emotion_suggestion(text, emotion):
    prompt = f"你是一位溫暖的 AI 心情導師，使用者剛剛輸入了以下文字：「{text}」，我們判斷他現在的心情是「{emotion}」。請用一句親切的中文話語給出簡短鼓勵或陪伴建議，語氣自然、不要說你是 AI，也不要重複情緒詞。"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=60
        )
        return response.choices[0].message['content'].strip()
    except:
        return "希望你今天過得更順利一點，加油！"

# --- Session 狀態 ---
if 'last_emotion' not in st.session_state:
    st.session_state.last_emotion = None
if 'last_song' not in st.session_state:
    st.session_state.last_song = None

# --- 分析並推薦 ---
if st.button("🎵 開始分析"):
    if user_input.strip() == "":
        st.warning("請輸入內容後再按下按鈕喔！")
    else:
        emotion = gpt_emotion_classifier(user_input) if method == "使用 GPT 模型（推薦）" else rule_based_emotion_classifier(user_input)
        song = random.choice(emotion_song_map.get(emotion, emotion_song_map["平淡"]))

        st.session_state.last_emotion = emotion
        st.session_state.last_song = song

        st.success(f"偵測到你現在的心情是 **{emotion}** 😌")
        st.markdown(f"🎶 推薦歌曲：**{song['title']}**")
        st.markdown(f"📜 歌詞片段：_{song['lyrics']}_")

        try:
            st.video(song["youtube"])
        except:
            st.warning("⚠️ 無法嵌入影片播放，請點下方連結觀看：")
        st.markdown(f"[▶️ 點我播放歌曲]({song['youtube']})", unsafe_allow_html=True)

        suggestion = gpt_emotion_suggestion(user_input, emotion)
        st.info(f"💬 {suggestion}")

if st.session_state.last_emotion and st.button("🎲 再推薦一首"):
    emotion = st.session_state.last_emotion
    last_song = st.session_state.last_song
    candidates = [s for s in emotion_song_map[emotion] if s != last_song]
    another_song = random.choice(candidates) if candidates else last_song

    st.session_state.last_song = another_song
    st.markdown(f"🎶 新推薦：**{another_song['title']}**")
    st.markdown(f"📜 歌詞片段：_{another_song['lyrics']}_")
    try:
        st.video(another_song["youtube"])
    except:
        st.warning("⚠️ 無法嵌入影片播放，請點下方連結觀看：")
    st.markdown(f"[▶️ 點我播放歌曲]({another_song['youtube']})", unsafe_allow_html=True)

# --- 猜歌小遊戲區塊 ---
st.markdown("---")
st.subheader("🎮 周杰倫猜歌挑戰（可選玩）")
st.write("根據下方歌詞片段猜出是哪一首周杰倫的歌～")

all_songs = [song for songs in emotion_song_map.values() for song in songs]

if 'quiz_song' not in st.session_state:
    st.session_state.quiz_song = random.choice(all_songs)
if 'answer_revealed' not in st.session_state:
    st.session_state.answer_revealed = False

st.markdown(f"📜 歌詞提示： _{st.session_state.quiz_song['lyrics']}_")
guess = st.text_input("你猜這是哪一首歌？")

if st.button("✅ 送出你的答案"):
    correct = st.session_state.quiz_song["title"]
    if guess.strip() == "":
        st.warning("請輸入歌名再提交喔～")
    elif guess.strip() == correct:
        st.success(f"🎉 答對啦！這首是《{correct}》！")
        st.session_state.answer_revealed = True
    else:
        st.error("答錯了，再試一次或看答案吧！")

if st.button("🤔 看答案"):
    st.info(f"✅ 正確答案是：**《{st.session_state.quiz_song['title']}》**")
    st.session_state.answer_revealed = True

if st.session_state.answer_revealed and st.button("🎲 換一題"):
    st.session_state.quiz_song = random.choice(all_songs)
    st.session_state.answer_revealed = False
    st.rerun()  # ✅ 改這行

