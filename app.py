import streamlit as st
from ai import generate_content
import base64
import html

# Set page configuration
st.set_page_config(page_title="Python File Summarizer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #fafafa;  /* Dark Blue */
        text-align: center;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 24px;
        color: #fafafa;  /* Medium Blue */
        margin-top: 20px;
    }
    .info-box {
        background-color: #fafafa;  /* Light Blue */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #00897b;  /* Teal */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #fafafa;  /* Darker Teal */
    }
    .scrollable-code {
        max-height: 300px;
        overflow-y: auto;
        background-color: #263238;  /* Dark Gray */
        padding: 10px;
        border-radius: 5px;
        white-space: pre-wrap;
        font-family: monospace;
        color: #ffffff;  /* White text */
    }
    .scrollable-summary {
        max-height: 400px;
        overflow-y: auto;
        background-color: #fafafa;  /* Soft White */
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        white-space: pre-wrap;
        color: #212121;  /* Dark Gray */
    }
    .stMarkdown, .stText {
        color: #fafafa;  /* Dark Blue */
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar for instructions and settings
with st.sidebar:
    st.header("Instructions")
    st.write("Upload a Python (.py) file to generate a beginner-friendly summary.")
    st.write("The summary will explain the code steps in a simple, research-oriented tone.")
    st.write("Download the summary as a text file after generation.")

# Main content
st.markdown('<div class="main-title">Python File Summarizer Dashboard</div>', unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns([2, 1])

# Left column: File upload and processing
with col1:
    st.markdown('<div class="section-header">Upload Your File</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a .py file", type=["py"], help="Select a Python file to analyze")

    # Prompt parameters (hidden from UI, used internally)
    prompt_parameters = """
    Parameters: 
    - Tone: Research Oriented
    - Writing technique: Student level, beginner friendly and explanatory 
    - Comma usage: very less 
    - Words that should not be used: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, 
        notably, utilized, utilize, foster, pivot, pivotal, robust, highlights, enhances, tailored, employed,
        finally, lastly, relevance, encompassed, reveals, generalizability, demonstrate, meticulously, paramount
    - Avoid technical jargon where possible and ensure readability.
    """

    if uploaded_file is not None:
        # Read and display file info
        file_content = uploaded_file.read().decode("utf-8")
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
        st.markdown('</div>', unsafe_allow_html=True)

        # Generate summary button
        if st.button("Generate Summary", key="generate"):
            prompt = prompt_parameters + f"""
            Summarize the work done in the code.
            Write headings of the steps, for each heading write 3 subheadings
            1. Explanation: explain the step in a line
            2. why: why we have used it in this code
            3. how: how will it contribute 
    
            Finally, give the definitions of all the algorithms getting used
    
            Instructions:
            - Paragraphs and next line separators should be correctly followed.
            - Don't write conclusion in the end.
            - Don't write anything which is not present in the code.
    
            Code to generate summary of:
            "{file_content}"
            """
            with st.spinner("Generating summary..."):
                output = generate_content(prompt)
                
                # Display summary in a scrollable container
                st.markdown('<div class="section-header">Generated Summary</div>', unsafe_allow_html=True)
                with st.expander("View Summary", expanded=True):
                    escaped_output = html.escape(output)
                    st.markdown(f'<div class="scrollable-summary">{escaped_output}</div>', unsafe_allow_html=True)

                # Download link
                def generate_download_link(text, filename="summary.txt"):
                    b64 = base64.b64encode(text.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Summary</a>'
                    return href
                
                st.markdown(generate_download_link(output), unsafe_allow_html=True)
    else:
        st.info("Please upload a .py file to start.")

# Right column: Preview and tips
with col2:
    st.markdown('<div class="section-header">File Preview</div>', unsafe_allow_html=True)
    if uploaded_file is not None:
        escaped_content = html.escape(file_content)
        st.markdown(f'<div class="scrollable-code">{escaped_content}</div>', unsafe_allow_html=True)
    else:
        st.write("No file uploaded yet.")
    
    st.markdown('<div class="section-header">Tips</div>', unsafe_allow_html=True)
    st.write("- Upload a valid .py file.")
    st.write("- Ensure the file is not empty.")
    st.write("- Summary will be simple and easy to read.")