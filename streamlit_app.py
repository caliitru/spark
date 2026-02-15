import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Page config
st.set_page_config(
    page_title="Spark Studio - Campaign Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API URL
BACKEND_URL = "http://localhost:8000"  # Change in production

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1337ec;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #0f2bbd;
    }
    .caption-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1337ec;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'input'

# Header
st.markdown('<div class="main-header">⚡ Spark Studio</div>', unsafe_allow_html=True)
st.markdown("### AI-Powered Social Media Campaign Generator")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Page navigation
    page = st.radio(
        "Navigation",
        ["Create Campaign", "View Results"],
        index=0 if st.session_state.current_page == 'input' else 1
    )
    
    st.markdown("---")
    st.info("💡 **Tip**: Fill in the campaign details and click Generate to create AI-powered content!")

# ============================================================================
# INPUT PAGE - Create Campaign
# ============================================================================

if page == "Create Campaign":
    st.session_state.current_page = 'input'
    
    # Platform selector
    st.subheader("📱 Platform")
    platform = st.selectbox(
        "Select your target platform",
        ["linkedin", "instagram", "twitter"],
        help="Platform selection influences formatting, hashtags, and tone"
    )
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Campaign Basics")
        
        company = st.text_input(
            "Brand Name *",
            placeholder="e.g., Spark Studio",
            help="Your company or brand name"
        )
        
        event = st.text_input(
            "Event / Campaign",
            placeholder="e.g., Product Launch",
            help="What's the campaign about?"
        )
        
        title = st.text_input(
            "Campaign Title",
            placeholder="e.g., Introducing AI Platform",
            help="Catchy title for your campaign"
        )
        
        campaign_message = st.text_area(
            "Campaign Message",
            placeholder="What is the primary story or offer you want to communicate?",
            help="Main message for your campaign",
            height=100
        )
        
        call_to_action = st.text_input(
            "Call to Action",
            placeholder="e.g., Shop Now, Sign Up Free",
            help="What action do you want users to take?"
        )
    
    with col2:
        st.subheader("🎯 Content Settings")
        
        target_audience = st.text_area(
            "Target Audience",
            placeholder="e.g., Marketing managers at B2B tech companies",
            help="Who is this content for?",
            height=80
        )
        
        product = st.text_input(
            "Product Name",
            placeholder="e.g., AI Marketing Platform",
            help="Specific product name (optional)"
        )
        
        product_description = st.text_area(
            "Product Description",
            placeholder="Describe your product in detail...",
            help="Detailed description of the product",
            height=100
        )
        
        style = st.text_input(
            "Visual Style",
            placeholder="e.g., modern, minimalist, bold",
            help="Desired visual style for images"
        )
        
        mood = st.text_input(
            "Mood / Vibe",
            placeholder="e.g., professional, energetic, innovative",
            help="What feeling should the content evoke?"
        )
        
        color = st.text_input(
            "Color Palette",
            placeholder="e.g., blue, white, gold",
            help="Color scheme for visuals"
        )
    
    # Additional options
    st.subheader("🔢 Generation Options")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        want_captions = st.checkbox("Generate Captions", value=True)
        if want_captions:
            num_captions = st.slider("Number of Captions", 1, 5, 3)
    
    with col4:
        want_images = st.checkbox("Generate Images", value=False)
        if want_images:
            num_images = st.slider("Number of Images", 1, 5, 3)
    
    with col5:
        username = st.text_input(
            "Username",
            value=f"User_{st.session_state.get('user_id', '001')}",
            help="Used for organizing generated files"
        )
    
    # Generate button
    st.markdown("---")
    
    if st.button("🚀 Generate Campaign", type="primary"):
        # Validation
        if not company:
            st.error("⚠️ Please fill in the Brand Name field!")
        elif not want_captions and not want_images:
            st.error("⚠️ Please select at least one output type (Captions or Images)!")
        else:
            # Prepare request
            request_data = {
                "username": username,
                "platform": platform,
                "company": company,
                "event": event or "",
                "title": title or "",
                "product_description": product_description or "",
                "num_images": num_images if want_images else 0,
                "num_captions": num_captions if want_captions else 0,
                "brand_name": company,
                "color": color or None,
                "want_images": want_images,
                "want_captions": want_captions,
                "Target_audience": target_audience or None,
                "Product": product or None,
                "Style": style or None,
                "campaign_message": campaign_message or None,
                "features": [],
                "layout": None,
                "mood": mood or None,
                "call_to_action": call_to_action or None
            }
            
            # Show request data for debugging
            with st.expander("🔍 Request Payload"):
                st.json(request_data)
            
            # Make API call
            with st.spinner("✨ Generating your campaign... This may take a moment!"):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=request_data,
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.generated_data = {
                            'result': result,
                            'input': request_data
                        }
                        st.session_state.current_page = 'results'
                        st.success("🎉 Campaign generated successfully!")
                        st.info("👉 Switch to 'View Results' in the sidebar to see your content!")
                        
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. The backend might be taking too long.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to backend. Make sure it's running at " + BACKEND_URL)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================================================
# OUTPUT PAGE - View Results
# ============================================================================

elif page == "View Results":
    st.session_state.current_page = 'results'
    
    if st.session_state.generated_data is None:
        st.warning("⚠️ No campaign generated yet. Please create a campaign first!")
        if st.button("← Go to Create Campaign"):
            st.session_state.current_page = 'input'
            st.rerun()
    else:
        result = st.session_state.generated_data['result']
        input_data = st.session_state.generated_data['input']
        
        # Campaign Summary Sidebar
        with st.sidebar:
            st.markdown("---")
            st.subheader("📊 Campaign Summary")
            st.write(f"**Platform:** {input_data['platform'].title()}")
            st.write(f"**Brand:** {input_data['company']}")
            st.write(f"**Target Audience:** {input_data['Target_audience'] or 'Not specified'}")
            st.write(f"**CTA:** {input_data['call_to_action'] or 'Not specified'}")
            
            if st.button("🔄 Generate New Campaign"):
                st.session_state.current_page = 'input'
                st.rerun()
        
        # Tabs for Captions and Images
        tabs = []
        if 'captions' in result:
            tabs.append("📝 Captions")
        if 'images' in result:
            tabs.append("🖼️ Images")
        
        if tabs:
            selected_tab = st.tabs(tabs)
            
            # Captions Tab
            if "📝 Captions" in tabs:
                with selected_tab[tabs.index("📝 Captions")]:
                    st.subheader(f"Generated Captions ({len(result['captions'])})")
                    
                    for i, caption in enumerate(result['captions'], 1):
                        with st.container():
                            st.markdown(f'<div class="caption-box">', unsafe_allow_html=True)
                            st.markdown(f"**Caption {i}**")
                            st.text_area(
                                f"caption_{i}",
                                value=caption,
                                height=150,
                                label_visibility="collapsed"
                            )
                            
                            col_a, col_b = st.columns([1, 4])
                            with col_a:
                                if st.button(f"📋 Copy", key=f"copy_{i}"):
                                    st.code(caption, language=None)
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.markdown("---")
            
            # Images Tab
            if "🖼️ Images" in tabs:
                with selected_tab[tabs.index("🖼️ Images")]:
                    st.subheader(f"Generated Images ({len(result['images'])})")
                    
                    # Display images
                    cols = st.columns(min(3, len(result['images'])))
                    
                    for i, img_filename in enumerate(result['images']):
                        with cols[i % 3]:
                            try:
                                # Try to load image from local path
                                img_path = f"{input_data['username']}_generated_images/{img_filename}"
                                
                                st.info(f"**Image {i+1}**")
                                st.write(f"Filename: `{img_filename}`")
                                st.write(f"Path: `{img_path}`")
                                
                                # Try to display image if it exists
                                try:
                                    img = Image.open(img_path)
                                    st.image(img, caption=f"Image {i+1}", use_container_width=True)
                                except:
                                    st.warning("Image file not found locally. Check backend logs.")
                                    # Show placeholder
                                    st.image("https://via.placeholder.com/512x512?text=Image+" + str(i+1))
                                
                                if st.button(f"⬇️ Download", key=f"download_{i}"):
                                    st.info("Download functionality coming soon!")
                                    
                            except Exception as e:
                                st.error(f"Error loading image: {str(e)}")
                    
                    st.markdown("---")
                    st.info("💡 **Note**: Images are saved locally by the backend. To display them here, you may need to add a static file serving endpoint to your FastAPI backend.")
        
        # Show raw response for debugging
        with st.expander("🔍 View Raw API Response"):
            st.json(result)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Built with Streamlit & FastAPI | Powered by OpenAI"
    "</div>",
    unsafe_allow_html=True
)