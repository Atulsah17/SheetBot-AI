import re
import os
from openai import OpenAI
from dotenv import load_dotenv
import ast
import streamlit as st

load_dotenv()

def generate_analysis_code(df, question, col_types):
    """Generate pandas/matplotlib code using OpenAI GPT-4o."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client:
        raise ValueError("Invalid OpenAI API key")
    sample = df.head(3).to_markdown(index=False)
    col_types_str = {col: dtype for col, dtype in col_types.items()}

    context = f"""
You are a data analyst. A user has uploaded a DataFrame with the following structure:

{sample}

Column types: {col_types_str}

Write clean and executable Python code using pandas to answer the question:

"{question}"

Guidelines:
- Use 'df' as the DataFrame variable.
- Handle missing values gracefully using pandas (e.g., dropna(), fillna()).
- If a plot is appropriate, use matplotlib (imported as plt).
- Do not use print() or markdown — just Python code.
- The final line should be an expression to evaluate (e.g., a variable or a plot).
- Ensure code is syntactically correct and safe.
- Use descriptive titles and labels for plots.

Only return plain Python code — no comments, markdown, or formatting.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You write and analyze pandas code."},
                {"role": "user", "content": context}
            ],
            temperature=0.0
        )
        raw_code = response.choices[0].message.content.strip()
        if raw_code.startswith("```"):
            raw_code = re.sub(r'^```(?:python)?\n|```$', '', raw_code)
        try:
            ast.parse(raw_code)
        except SyntaxError as e:
            st.error(f"Error: Invalid code generated: {str(e)}")
            return None
        if not raw_code:
            return None
        return raw_code.strip()
    except Exception as e:
        st.error(f"Error generating code: {str(e)}")
        return None