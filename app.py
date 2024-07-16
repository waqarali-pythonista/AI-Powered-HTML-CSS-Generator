import streamlit as st
from openai import OpenAI
import base64

# Function to encode image in base64
def encode_image(image):
    return base64.b64encode(image.read()).decode('utf-8')

# Function to create the HTML and CSS based on the image
def generate_html_css(base64_image):
    # Assuming your OpenAI client setup here
    MODEL = "gpt-4o"
    api_key = ""
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me with create the html and css page but don't any other text just give me code "},
            {"role": "user", "content": [
                {"type": "text", "text": f"create the html and css page according this {base64_image} image"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

st.title('Code Generator ')

# File uploader for image input
uploaded_file = st.file_uploader("Upload an image (PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

    # Encode the image to base64
    base64_image = encode_image(uploaded_file)
    
    # Generate HTML and CSS
    if st.button('Generate '):
        html_css_content = generate_html_css(base64_image)
        
        # Display the generated HTML and CSS
        st.markdown("### Generated HTML & CSS")
        st.code(html_css_content, language='html')
        
        # Create a download button
        st.download_button(
            label="Download HTML & CSS",
            data=html_css_content,
            file_name='output.html',
            mime='text/html'
        )
