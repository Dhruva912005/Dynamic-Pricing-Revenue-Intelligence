"""
Notebook Executor Script
Executes all Jupyter notebooks in place so that charts, outputs, tables, and serialized models
are fully computed and embedded in the .ipynb files.
"""

import nbformat
from nbclient import NotebookClient
import os
import sys

def execute_notebook(nb_path):
    print(f"\n==========================================")
    print(f"Executing {nb_path}...")
    print(f"==========================================")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        
    cwd = os.path.abspath(".")
    client = NotebookClient(nb, timeout=600, kernel_name='python3', resources={'metadata': {'path': cwd}})
    client.execute()
    
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Successfully executed and saved {nb_path}.")

if __name__ == "__main__":
    notebooks = [
        "01_Sales_Analysis.ipynb",
        "02_Demand_Forecasting.ipynb",
        "03_Dynamic_Pricing_Optimization.ipynb"
    ]
    for nb in notebooks:
        try:
            execute_notebook(nb)
        except Exception as e:
            print(f"Error executing {nb}: {e}")
            sys.exit(1)
    print("\nAll notebooks executed with 100% success!")
