from PIL import Image
import io
from io import BytesIO

import streamlit as st

st.set_page_config(
    page_title="Pushitabi GIF Tool",
    layout="wide"
)
def trim_transparent_margin(img):

    rgba_img = img.convert("RGBA")

    alpha = rgba_img.getchannel("A")

    bbox = alpha.getbbox()

    if bbox is None:
        return rgba_img

    return rgba_img.crop(bbox)


def generate_gif_buffer(
    background_img,
    loaded_characters
):

    import io

    frames = []
    durations = []

    for character in loaded_characters:

        frame = background_img.copy()

        character_img = character["image"]

        adjust = int(
            character["adjust"]
        )

        st.write(
            f"adjust値: {adjust}"
        )

        new_width = int(
            300 * (100 + adjust) / 100
        )

        new_height = int(
            character_img.height
            * new_width
            / character_img.width
        )

        character_img = character_img.resize(
            (new_width, new_height)
        )

        x = (
            (
                frame.width
                - character_img.width
            ) // 2
        ) + character["x"]

        y = (
            (
                frame.height
                - character_img.height
            ) // 2
        ) + character["y"]

        frame.paste(
            character_img,
            (x, y),
            character_img
        )
        frames.append(
            frame.convert("RGBA")
        )

        durations.append(
            character["duration"] * 1000
        )

    gif_buffer = io.BytesIO()

    frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0
    )

    gif_buffer.seek(0)

    return gif_buffer

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

character_settings = []

if character_files:

    st.subheader("キャラクター設定")

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
            x_adjust = st.slider(
                f"X位置_{index}",
                min_value=-500,
                max_value=500,
                value=0,
                step=10
            )

            y_adjust = st.slider(
                f"Y位置_{index}",
                min_value=-500,
                max_value=500,
                value=0,
                step=10
            )

            character_settings.append(
                {
                    "file_name": character_file.name,
                    "order": display_order,
                    "duration": display_time,
                    "adjust": size_adjust,
                    "x": x_adjust,
                    "y": y_adjust
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

        for index, character_file in enumerate(
            character_files,
            start=1
        ):
            img = Image.open(
                character_file
            ).convert("RGBA")

            img = trim_transparent_margin(
                img
            )

            loaded_characters.append(
                {
                    "file_name": character_file.name,
                    "image": img,
                    "order": character_settings[
                        index - 1
                    ]["order"],
                    "duration": character_settings[
                        index - 1
                    ]["duration"],
                    "adjust": character_settings[
                        index - 1
                    ]["adjust"],
                    "x": character_settings[
                        index - 1
                    ]["x"],
                    "y": character_settings[
                        index - 1
                    ]["y"]
                }
            )


        st.write(
            f"読込キャラ数: {len(loaded_characters)}"
        )

        loaded_characters.sort(
            key=lambda x: x["order"]
        )

        st.write(
            "並び替え完了"
        )

        gif_buffer = generate_gif_buffer(
            background_img,
            loaded_characters
        )

        st.success(
            "GIF生成成功"
        )

        st.image(
            gif_buffer.getvalue()
        )
