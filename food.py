"""
Food Recognition and Calorie Counter using Groq Vision API
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import base64
import io
import json
import re
from PIL import Image
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px

# Configure Groq API
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

def get_base64_of_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def parse_json_response(text):
    """
    Attempt to extract and parse JSON from the text response
    """
    try:
        # First try to find a JSON block in the text
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(text)
    except Exception as e:
        return None

def get_food_analysis(image):
    """
    Analyze food image and return calorie and nutritional information
    """
    base64_image = get_base64_of_image(image)
    
    prompt = """Please analyze this food image and provide nutritional information in valid JSON format.
    The response MUST be a pure JSON object without markdown formatting or backticks.
    
    Structure the JSON as follows:
    {
        "food_items": ["item1", "item2"],
        "estimated_calories": 500,
        "macros": {
            "protein": 30,
            "carbs": 50,
            "fats": 20
        },
        "summary": "A detailed text description of the food, portion size, and health tips.",
        "detailed_analysis": "Detailed list of ingredients and their approximate contribution."
    }
    
    Ensure all numerical values are integers or floats (no units like 'g' or 'kcal' in the number fields).
    """
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.3, # Lower temperature for better JSON consistency
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize Streamlit app
st.set_page_config(
    page_title="Food Recognition & Calorie Counter",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Food Recognition & Calorie Counter")
st.markdown("Upload a photo of your food to identify it and get calorie information!")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Food Photo")
    uploaded_file = st.file_uploader(
        "Choose a food image...",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear photo of your food"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Food Photo", use_column_width=True)

with col2:
    st.subheader("Analysis Results")
    
    if uploaded_file is not None:
        if st.button("🔍 Analyze Food & Get Calories", key="analyze_btn"):
            with st.spinner("Analyzing your food..."):
                # Handle images with alpha channel
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                
                raw_response = get_food_analysis(image)
                parsed_data = parse_json_response(raw_response)
                
                if parsed_data:
                    # Display Text Summary
                    st.markdown("### 🥗 Food Summary")
                    st.write(parsed_data.get("summary", "No summary available."))
                    
                    st.markdown(f"**Estimated Calories:** {parsed_data.get('estimated_calories', 'N/A')} kcal")
                    
                    # Create columns for charts
                    chart_col1, chart_col2 = st.columns(2)
                    
                    macros = parsed_data.get("macros", {})
                    if macros:
                        with chart_col1:
                            st.subheader("Macro Distribution")
                            # Pie Chart
                            labels = list(macros.keys())
                            values = list(macros.values())
                            
                            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                            st.plotly_chart(fig_pie, use_container_width=True)
                        
                        with chart_col2:
                            st.subheader("Nutritional Values (g)")
                            # Bar Chart
                            fig_bar = px.bar(
                                x=list(macros.keys()),
                                y=list(macros.values()),
                                labels={'x': 'Nutrient', 'y': 'Grams'},
                                color=list(macros.keys())
                            )
                            fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, showlegend=False)
                            st.plotly_chart(fig_bar, use_container_width=True)
                    
                    with st.expander("See Detailed Analysis"):
                        st.write(parsed_data.get("detailed_analysis", ""))
                        st.json(parsed_data) # Show raw data for transparency
                        
                else:
                    # Fallback if JSON parsing fails
                    st.error("Could not parse structured data. Showing raw response:")
                    st.markdown(raw_response)
                
                # Add download option for raw response
                st.download_button(
                    label="📥 Download Analysis",
                    data=raw_response,
                    file_name="food_analysis.txt",
                    mime="text/plain"
                )
    else:
        st.info("👆 Upload an image to get started!")

# Footer with instructions
st.markdown("---")
st.markdown("""
### 📝 How to use:
1. Click on "Choose a food image" to upload a photo of your food
2. Click "Analyze Food & Get Calories" to get detailed analysis
3. The AI will identify the food and provide graphs (Pie & Bar charts) of the nutritional breakdown.

### ⚡ Tips for best results:
- Use clear, well-lit photos
- Include the entire portion in the frame
""")
