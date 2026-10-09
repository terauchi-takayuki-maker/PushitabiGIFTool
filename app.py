from PIL import Image
import io
from io import BytesIO

import streamlit as st

st.set_page_config(
    page_title="Pushitabi GIF Tool",
    layout="wide"
)

st.title("🚄 Pushitabi GIF Generator")

# ----------------------------
# 背景画像
# ----------------------------

background_file = st.file_uploader(
    "背景画像",
    type=["png", "jpg", "jpeg"]
)

# ----------------------------
# キャラクター画像
# ----------------------------

character_files = st.file_uploader(
    "キャラクター画像",
    type=["png"],
    accept_multiple_files=True
)

# ----------------------------
# キャラクター設定
# ----------------------------

if character_files:

    st.subheader("キャラクター設定")

    character_settings = []

    for index, character_file in enumerate(
        character_files,
        start=1
    ):

        st.markdown("---")

        col1, col2 = st.columns(
            [1, 2]
        )

        with col1:

            st.image(
                character_file,
                width=150
            )

        with col2:

            st.write(
                f"ファイル名: {character_file.name}"
            )

            display_order = st.number_input(
                f"表示順_{index}",
                min_value=1,
                value=index
            )

            display_time = st.number_input(
                f"表示時間(秒)_{index}",
                min_value=0.1,
                value=0.5,
                step=0.1
            )

            size_adjust = st.slider(
                f"サイズ補正_{index}",
                min_value=-50,
                max_value=50,
                value=0,
                step=5
            )

            character_settings.append(
                {
                    "file_name": character_file.name,
                    "order": display_order,
                    "duration": display_time,
                    "adjust": size_adjust
                }
            )

    st.markdown("---")

    st.subheader("現在の設定")

    st.json(character_settings)
# ----------------------------
# GIF生成ボタン
# ----------------------------

if st.button("GIF生成"):

    if not background_file:

        st.error(
            "背景画像を選択してください"
        )

    elif not character_files:

        st.error(
            "キャラクター画像を選択してください"
        )

    else:

        st.success(
            "GIF生成テスト成功"
        )

        st.write(
            f"背景画像: {background_file.name}"
        )

        st.write(
            f"キャラクター数: {len(character_files)}"
        )
        background_img = Image.open(
            background_file
        ).convert("RGBA")

        st.image(
            background_img,
            caption="背景画像",
            width=300
        )
        loaded_characters = []

        for character_file in character_files:

            img = Image.open(
                character_file
            ).convert("RGBA")

           loaded_characters.append(
    {
        "file_name": character_file.name,
        "image": img,
        "order": character_settings[
            len(loaded_characters)
        ]["order"],
        "duration": character_settings[
            len(loaded_characters)
        ]["duration"],
        "adjust": character_settings[
            len(loaded_characters)
        ]["adjust"]
    }
)

        st.write(
            f"読込キャラ数: {len(loaded_characters)}"
        )
