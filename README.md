# SheetBot-AI

A conversational Excel analysis tool that transforms data into insights using natural language queries. SheetBot-AI showcases a unique cosmic-themed interface, robust data processing, and thoughtful design to demonstrate analytical thinking, creativity, and problem-solving skills.

## Overview

SheetBot-AI empowers users to upload Excel files (.xlsx) and ask questions like "What is the average salary?" or "Show a bar chart of sales by region." With a modular architecture and a custom-designed UI featuring a cosmic dark gradient theme, the tool handles diverse datasets with mixed types and missing values. Key features include a large query input, downloadable results, a data summary dashboard, and a branded error system, ensuring an intuitive and professional experience.

## Features

- **Schema-Agnostic Processing**: Analyzes Excel files (up to 500 rows, 10–20 columns) with automatic detection of column types (numeric, string, datetime, binary).
- **Natural Language Queries**: Supports statistical summaries, filtered queries, comparisons, and visualizations through a prominent query bar.
- **Custom UI**: Features a cosmic dark gradient theme, branded cards with hover effects, a large query input (60px height), and a progress bar for query processing.
- **Data Summary**: Displays a dashboard with record count, field count, and numeric fields after file upload.
- **Export Options**: Download query results as CSV (tables), PNG (charts), or CSV (chat history).
- **Error Handling**: Custom-styled error messages in a branded red card for user-friendly feedback.
- **Robustness**: Handles edge cases like invalid files, empty queries, and missing data with clear error messages.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Atulsah17/SheetBot-AI
   cd neostats-assistant
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   - Create a `.env` file in the root directory with your API key (excluded via `.gitignore`).
   - Contact the project owner for the required API key format.

5. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   Open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. **Upload an Excel File**:
   - Use the sidebar to upload an `.xlsx` file (e.g., `employee_data.xlsx` with columns like `employee_id`, `salary`, `department`).
2. **View Data Summary**:
   - Check the “Data Overview” card for record count, fields, and numeric fields.
3. **Preview Data**:
   - See the first five rows in the “Data Snapshot” card.
4. **Ask Questions**:
   - Enter queries in the large query bar (e.g., “What is the average salary?”, “Show a bar chart of salary by department”).
   - View results as text, tables, or charts in the “Insight Results” card.
5. **Export Results**:
   - Download tables as `table.csv`, charts as `chart.png`, or query history as `history.csv`.
6. **Handle Errors**:
   - Custom error messages guide you if queries fail or files are invalid.

### Example Queries
- **Statistical**: “How many employees have a salary above 100,000?”
- **Visualization**: “Show a line chart of sales over time.”
- **Summary**: “What is the maximum performance score?”

## Directory Structure

```
Excel-assistant/
├── src/
│   ├── __init__.py
│   ├── preprocess.py
│   ├── query_parser.py
│   ├── data_processor.py
├── requirements.txt
├── .gitignore
├── app.py
├── README.md
```

## Screenshots

[![alt text](<Screenshot (132).png>)]
- Upload interface in sidebar.
- Data summary and preview cards.
- Query input and result with chart export.
- Custom error message example.

