import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from src.preprocess import load_and_clean_excel
from src.query_parser import generate_analysis_code
from src.data_processor import execute_code

# Set page config FIRST
st.set_page_config(page_title="Excel Assistant", layout="wide")

# Dark gradient theme CSS with larger query bar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    .main { 
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
        color: #ffffff; 
        font-family: 'Inter', sans-serif; 
        padding: 20px; 
    }
    .stButton>button { 
        background: #3b82f6; 
        color: white; 
        border-radius: 8px; 
        padding: 10px 20px; 
        transition: all 0.3s ease; 
        border: none; 
    }
    .stButton>button:hover { 
        background: #1d4ed8; 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3); 
    }
    .stTextInput>div>input { 
        border-radius: 8px; 
        border: 1px solid #4b5563; 
        padding: 16px; 
        background: #374151; 
        color: #ffffff; 
        transition: border-color 0.3s ease; 
        font-size: 1.2rem; 
        height: 60px; 
    }
    .stTextInput>div>input:focus { 
        border-color: #3b82f6; 
        box-shadow: 0 0 8px rgba(59, 130, 246, 0.5); 
    }
    .stDataFrame { 
        border: 1px solid #4b5563; 
        border-radius: 8px; 
        background: #374151; 
        color: #ffffff; 
        padding: 10px; 
    }
    h1 { 
        color: #ffffff; 
        font-weight: 700; 
        font-size: 2.5rem; 
        display: flex; 
        align-items: center; 
        gap: 10px; 
    }
    h2 { 
        color: #e5e7eb; 
        font-weight: 600; 
        font-size: 1.5rem; 
    }
    .sidebar .stFileUploader { 
        background: #374151; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #4b5563; 
    }
    .stMetricLabel, .stMetricValue { 
        color: #ffffff !important; 
        font-family: 'Inter', sans-serif; 
    }
    .stSpinner { 
        color: #3b82f6; 
    }
    .card { 
        background: #374151; 
        border-radius: 8px; 
        padding: 20px; 
        margin-bottom: 20px; 
        border: 1px solid #4b5563; 
        transition: transform 0.3s ease; 
    }
    .card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2); 
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'col_types' not in st.session_state:
    st.session_state.col_types = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.markdown("""
    <h1><i class="fas fa-table"></i> Excel Assistant</h1>
    <p style="color: #d1d5db;">Upload an Excel file to unlock insights with natural language queries.</p>
""", unsafe_allow_html=True)

# Sidebar for file upload
with st.sidebar:
    st.markdown("<h2><i class='fas fa-upload'></i> Data Upload</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose Excel (.xlsx)", type=["xlsx"])
    if uploaded_file:
        try:
            st.session_state.df, st.session_state.col_types = load_and_clean_excel(uploaded_file)
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Main content
if st.session_state.df is not None:
    # Data Summary Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h2><i class='fas fa-info-circle'></i> Data Summary</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(st.session_state.df))
        with col2:
            st.metric("Columns", len(st.session_state.df.columns))
        with col3:
            st.metric("Numeric Columns", len([col for col, dtype in st.session_state.col_types.items() if dtype in ['int', 'float']]))
        st.markdown('</div>', unsafe_allow_html=True)

    # Data Preview Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h2><i class='fas fa-eye'></i> Data Preview</h2>", unsafe_allow_html=True)
        st.dataframe(st.session_state.df.head(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Query Input Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h2><i class='fas fa-question-circle'></i> Ask a Question</h2>", unsafe_allow_html=True)
        query = st.text_input(
            label="Enter your query",
            placeholder="e.g., What is the average salary?",
            key="query_input",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if query:
            # Progress Indicator
            progress_bar = st.progress(0)
            with st.spinner("Processing..."):
                try:
                    progress_bar.progress(30)
                    code = generate_analysis_code(st.session_state.df, query, st.session_state.col_types)
                    if not code:
                        raise ValueError("Failed to generate valid code")
                    progress_bar.progress(60)
                    result, fig = execute_code(code, st.session_state.df)
                    progress_bar.progress(100)

                    response_text = ""
                    if isinstance(result, (int, float)):
                        response_text = f"{result:,.2f}"
                    elif isinstance(result, pd.DataFrame):
                        response_text = "DataFrame displayed below"
                    elif isinstance(result, str) and "Error" in result:
                        response_text = result
                    elif result is not None:
                        response_text = str(result)

                    st.session_state.chat_history.append({
                        "question": query,
                        "response": response_text
                    })

                    # Answer Card
                    with st.container():
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown("<h2><i class='fas fa-check-circle'></i> Answer</h2>", unsafe_allow_html=True)
                        if isinstance(result, str) and "Error" in result:
                            st.error(response_text)
                        elif fig:
                            st.pyplot(fig)
                            # Export Chart
                            buf = io.BytesIO()
                            fig.savefig(buf, format="png", bbox_inches="tight")
                            buf.seek(0)
                            st.download_button(
                                label="Download Chart",
                                data=buf,
                                file_name="chart.png",
                                mime="image/png"
                            )
                            plt.clf()
                            plt.close(fig)  # Close figure to prevent warning
                        elif isinstance(result, pd.DataFrame):
                            st.dataframe(result, use_container_width=True)
                            # Export Table
                            csv = result.to_csv(index=False)
                            st.download_button(
                                label="Download Table",
                                data=csv,
                                file_name="result.csv",
                                mime="text/csv"
                            )
                        elif isinstance(result, (int, float)):
                            st.metric(label="Answer", value=f"{result:,.2f}")
                        elif result is not None:
                            st.success(response_text)
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.chat_history.append({
                        "question": query,
                        "response": f"Error: {str(e)}"
                    })
                    progress_bar.progress(100)

    # Chat History Download Card
    if st.session_state.chat_history:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h2><i class='fas fa-history'></i> Chat History</h2>", unsafe_allow_html=True)
            chat_df = pd.DataFrame([{
                "Query": h["question"],
                "Response": h["response"]
            } for h in st.session_state.chat_history])
            chat_csv = chat_df.to_csv(index=False)
            st.download_button(
                label="Download Chat History",
                data=chat_csv,
                file_name="chat_history.csv",
                mime="text/csv"
            )
            st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("Please upload an Excel file to start.")
        st.markdown('</div>', unsafe_allow_html=True)