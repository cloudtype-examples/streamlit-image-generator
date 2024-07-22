import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

def generate_image_with_dalle(api_key, prompt, size):
    try:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"이미지 생성 중 오류 발생: {str(e)}")
        return None

def main():
    st.title("DALL-E 이미지 생성기")

    api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")
    
    prompt = st.text_input("이미지 생성을 위한 설명을 입력하세요:")
    
    aspect_ratio = st.selectbox("이미지 비율 선택:", ["정사각형", "가로", "세로"])
    
    if aspect_ratio == "정사각형":
        size_options = ["1024x1024"]
    elif aspect_ratio == "가로":
        size_options = ["1792x1024", "1024x576"]
    else:  # 세로
        size_options = ["1024x1792", "576x1024"]
    
    size = st.selectbox("이미지 크기 선택:", size_options)

    if st.button("이미지 생성"):
        if not api_key:
            st.warning("OpenAI API 키를 입력해주세요.")
        elif not prompt:
            st.warning("이미지 설명을 입력해주세요.")
        else:
            with st.spinner("DALL-E를 사용하여 이미지 생성 중..."):
                image = generate_image_with_dalle(api_key, prompt, size)
                if image:
                    st.image(image, caption=f"생성된 이미지: {prompt}", use_column_width=True)
                    
                    buf = BytesIO()
                    image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="이미지 다운로드",
                        data=byte_im,
                        file_name=f"generated_image_{prompt[:20]}.png",
                        mime="image/png"
                    )

if __name__ == "__main__":
    main()