from PIL import Image
import io

import streamlit as st

# GIF生成用
from io import BytesIO

st.set_page_config(
    page_title="Pushitabi GIF Tool",
    layout="wide"
)

st.title("🚄 Pushitabi GIF Generator")
# ==========================================
# 透明余白削除
# ==========================================
# ==========================================
# 透明余白削除
# ==========================================

def trim_transparent_margin(img):

    rgba_img = img.convert("RGBA")

    alpha = rgba_img.getchannel("A")

    bbox = alpha.getbbox()

    if bbox is None:
        return rgba_img

    return rgba_img.crop(bbox)


# ==========================================
# GIF生成
# ==========================================

def generate_gif_buffer(
    background_img,
    character_data
):

    CANVAS_SIZE = 1200
    FIT_MARGIN = 60

    frames = []
    durations = []

    for item in character_data:

        frame = background_img.copy()

        character_img = item["image"]

        character_img = trim_transparent_margin(
            character_img
        )

        original_width, original_height = (
            character_img.size
        )

        available_width = (
            CANVAS_SIZE - FIT_MARGIN * 2
        )

        available_height = (
            CANVAS_SIZE - FIT_MARGIN * 2
        )

        fit_scale = min(
            available_width / original_width,
            available_height / original_height
        )

        adjustment = item["adjust"]

        adjustment_scale = (
            1 + adjustment / 100
        )

        final_scale = (
            fit_scale * adjustment_scale
        )

        target_width = max(
            1,
            round(
                original_width * final_scale
            )
        )

        target_height = max(
            1,
            round(
                original_height * final_scale
            )
        )

        resized_character = character_img.resize(
            (
                target_width,
                target_height
            ),
            Image.Resampling.LANCZOS
        )

        position_x = (
            CANVAS_SIZE - target_width
        ) // 2

        position_y = (
            CANVAS_SIZE - target_height
        ) // 2

        frame.alpha_composite(
            resized_character,
            (
                position_x,
                position_y
            )
        )

        frames.append(
            frame.convert("RGB")
        )

        durations.append(
            int(
                item["duration"] * 1000
            )
        )

    gif_buffer = BytesIO()

    frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2
    )

    gif_buffer.seek(0)

    return gif_buffer
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

        background_img = Image.open(
            background_file
        ).convert("RGBA")

        background_img = background_img.resize(
            (1200, 1200)
        )

        loaded_characters = []

        for character_file in character_files:

            img = Image.open(
                character_file
            ).convert("RGBA")

            loaded_characters.append(
                {
                    "file_name": character_file.name,
                    "image": img
                }
            )

        st.success(
            "画像読込成功"
        )

        st.write(
            f"背景画像: {background_file.name}"
        )

        st.write(
            f"キャラクター数: {len(loaded_characters)}"
        )

        st.image(
            background_img,
            caption="背景画像",
            width=300
        )
        # --------------------------
        # 背景画像読込
        # --------------------------

        background_img = Image.open(
            background_file
        ).convert("RGBA")

        background_img = background_img.resize(
            (1200, 1200)
        )

        # --------------------------
        # キャラ画像読込
        # --------------------------

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

        st.success(
            "画像読込成功"
        )

        st.write(
            f"背景画像: {background_file.name}"
        )

        st.write(
            f"キャラクター数: {len(loaded_characters)}"
        )

       loaded_characters.sort(
       key=lambda x: x["order"]
       )
　　　　gif_buffer = generate_gif_buffer(
    key=lambda x: x["order"]
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

st.download_button(
    "GIFダウンロード",
    data=gif_buffer.getvalue(),
    file_name="pushitabi.gif",
    mime="image/gif"
)
