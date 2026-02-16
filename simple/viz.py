# viz_colab.py - Modified for Google Colab
import json
import numpy as np
from IPython.display import HTML, display
import base64

class Viz:
    def __init__(self):
        self.data = {}
    
    def add(self, name, data):
        """Add data (converts numpy to lists)"""
        if isinstance(data, np.ndarray):
            data = data.tolist()
        self.data[name] = data
        return self
    
    def show(self, width=900, height=600):
        """Display inline in Colab"""
        try:
            with open('viz.html', 'r') as f:
                html_template = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Template file 'viz.html' not found.")
        
        try:
            with open('viz.js', 'r') as f:
                js_code = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Template file 'viz.js' not found.")
        
        # Embed data and JS inline
        data_json = json.dumps(self.data)
        
        # Replace the data fetch with inline data
        html_template = html_template.replace(
            "const data = await fetch('data.json').then(r => r.json());",
            f"const data = {data_json};"
        )
        
        # Replace the JS import with inline code
        html_template = html_template.replace(
            "import { createVisualization } from './viz.js';",
            f"{js_code}\n// Inline viz.js content above"
        )
        
        # Wrap in iframe with proper sizing
        iframe_html = f"""
        <iframe 
            srcdoc="{html_template.replace('"', '&quot;')}" 
            width="{width}" 
            height="{height}" 
            frameborder="0"
            style="border: 1px solid #ccc;">
        </iframe>
        """
        
        display(HTML(iframe_html))
        return self
    
    '''
    def save(self, filename='viz_export.html'):
        """Export single HTML file with embedded data"""
        try:
            with open('viz.html', 'r') as f:
                html = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Template file 'viz.html' not found.")
        
        try:
            with open('viz.js', 'r') as f:
                js = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Template file 'viz.js' not found.")
        
        # Embed data and JS
        data_json = json.dumps(self.data)
        
        html = html.replace(
            "const data = await fetch('data.json').then(r => r.json());",
            f"const data = {data_json};"
        )
        
        html = html.replace(
            "import { createVisualization } from './viz.js';",
            f"{js}\n// Inline viz.js content above"
        )
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"✅ Saved to {filename}")
        return self
    '''
