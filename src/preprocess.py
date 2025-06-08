import pandas as pd

def load_and_clean_excel(file):
    """Load and preprocess Excel file."""
    try:
        df = pd.read_excel(file)
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
        df = df.fillna(pd.NA)
        col_types = {}
        for col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    col_types[col] = 'float' if df[col].dtype in ['float64', 'float32'] else 'int'
                elif df[col].dropna().isin(['Yes', 'No', 'yes', 'no', 0, 1, True, False]).all():
                    col_types[col] = 'binary'
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    col_types[col] = 'datetime'
                else:
                    col_types[col] = 'string'
            except Exception:
                col_types[col] = 'string'
        return df, col_types
    except Exception as e:
        raise ValueError(f"Failed to load Excel file: {str(e)}")