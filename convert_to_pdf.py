#!/usr/bin/env python3
"""
Convert Jupyter notebook to PDF excluding code cells.
Keeps markdown cells and outputs from code cells.
"""

import json
import sys
import subprocess
from pathlib import Path

def filter_notebook(input_path, output_path):
    """Filter notebook to remove code source but keep markdown and outputs."""
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    new_cells = []
    
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            # Keep all markdown cells as-is
            new_cells.append(cell)
        elif cell['cell_type'] == 'code':
            # For code cells, remove the source but keep outputs
            new_cell = cell.copy()
            new_cell['source'] = []  # Remove source code
            # Keep outputs as-is
            new_cells.append(new_cell)
        else:
            # Keep other cell types as-is
            new_cells.append(cell)
    
    notebook['cells'] = new_cells
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    return output_path

def convert_to_pdf(notebook_path, output_pdf_path):
    """Convert notebook to PDF using nbconvert via HTML (avoids pandoc requirement)."""
    try:
        # First, convert to HTML with code excluded
        html_path = output_pdf_path.with_suffix('.html')
        cmd_html = [
            'jupyter', 'nbconvert',
            '--to', 'html',
            '--output', str(html_path.stem),
            str(notebook_path),
            '--TemplateExporter.exclude_input=True',
            '--TemplateExporter.exclude_input_prompt=True',
            '--no-prompt'
        ]
        
        result = subprocess.run(cmd_html, capture_output=True, text=True, check=True)
        print(f"Created HTML: {html_path}")
        
        # Try to convert HTML to PDF using playwright
        try:
            from playwright.sync_api import sync_playwright
            print("Converting HTML to PDF using playwright...")
            html_abs_path = html_path.resolve()
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file://{html_abs_path}')
                page.pdf(path=str(output_pdf_path), format='A4', print_background=True)
                browser.close()
            print(f"Successfully converted to PDF: {output_pdf_path}")
            html_path.unlink()  # Clean up HTML
            return True
        except ImportError:
            print("\nplaywright is not installed. Installing...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'playwright'], 
                         capture_output=True, check=True)
            subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'],
                         capture_output=True, check=True)
            from playwright.sync_api import sync_playwright
            print("Converting HTML to PDF using playwright...")
            html_abs_path = html_path.resolve()
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file://{html_abs_path}')
                page.pdf(path=str(output_pdf_path), format='A4', print_background=True)
                browser.close()
            print(f"Successfully converted to PDF: {output_pdf_path}")
            html_path.unlink()  # Clean up HTML
            return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting: {e.stderr}")
        if 'html_path' in locals() and html_path.exists():
            print(f"\nHTML file saved at: {html_path}")
            print("You can manually convert it to PDF by opening in a browser and printing to PDF.")
        return False
    except FileNotFoundError:
        print("Error: jupyter nbconvert not found. Please install it with: pip install nbconvert")
        return False
    except Exception as e:
        print(f"Error: {e}")
        if 'html_path' in locals() and html_path.exists():
            print(f"\nHTML file saved at: {html_path}")
            print("You can manually convert it to PDF by opening in a browser and printing to PDF.")
        return False

def main():
    input_notebook = Path('pipeline2.ipynb')
    filtered_notebook = Path('pipeline2_filtered.ipynb')
    output_pdf = Path('pipeline2.pdf')
    
    if not input_notebook.exists():
        print(f"Error: {input_notebook} not found")
        sys.exit(1)
    
    print(f"Filtering notebook to remove code cells: {input_notebook}")
    filter_notebook(input_notebook, filtered_notebook)
    
    print(f"Converting filtered notebook to PDF...")
    if convert_to_pdf(filtered_notebook, output_pdf):
        print(f"\n✓ PDF successfully created: {output_pdf}")
        # Clean up filtered notebook
        filtered_notebook.unlink()
    else:
        print("\nConversion failed. Filtered notebook saved at:", filtered_notebook)
        sys.exit(1)

if __name__ == '__main__':
    main()

