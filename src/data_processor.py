import pandas as pd
import matplotlib.pyplot as plt
import traceback

def execute_code(code, df):
    """Safely execute generated code."""
    local_env = {'df': df.copy(), 'pd': pd, 'plt': plt}
    result = None
    fig = None

    try:
        lines = code.strip().split('\n')
        if not lines:
            return None, "No code to execute."

        *body, last = lines

        with open("debug_code.txt", "a") as f:
            f.write(f"Code:\n{code}\n{'-'*50}\n")

        exec('\n'.join(body), {}, local_env)

        try:
            result = eval(last, {}, local_env)
        except SyntaxError:
            exec(last, {}, local_env)

        if plt.get_fignums():
            fig = plt.gcf()

        return result, fig

    except Exception as e:
        error_trace = traceback.format_exc()
        with open("debug_code.txt", "a") as f:
            f.write(f"Error:\n{error_trace}\n{'-'*50}\n")
        return None, f"Error: {str(e)}"