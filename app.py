import streamlit as st

st.set_page_config(
    page_title="Pushitabi GIF Tool",
    layout="wide"
)

st.title("🚄 Pushitabi GIF Generator")

st.write("Streamlit接続テスト")

background_file = st.file_uploader(
    "背景画像",
    type=["png", "jpg", "jpeg"]
)

character_files = st.file_uploader(
    "キャラクター画像",
    type=["png"],
    accept_multiple_files=True
)

if background_file:
    st.success("背景画像を読み込みました")

if character_files:
    st.success(
        f"{len(character_files)}件のキャラクター画像を読み込みました"
    )
