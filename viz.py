# viz.py
import json
import numpy as np
from IPython.display import IFrame

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
        """Save data and display"""
        # Save data
        try:
            with open('data.json', 'w') as f:
                json.dump(self.data, f)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to serialize data to JSON. Check that all data is JSON-serializable: {e}")
        
        # Display
        return IFrame('viz.html', width=width, height=height)
    
    def save(self, filename='viz_export.html'):
        """Export single HTML file with embedded data"""
        try:
            with open('viz.html', 'r') as f:
                html = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Template file 'viz.html' not found. Ensure viz.html is in the working directory.")
        
        try:
            with open('viz.js', 'r') as f:
                js = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Template file 'viz.js' not found. Ensure viz.js is in the working directory.")
        
        # Embed data and JS
        data_json = json.dumps(self.data)
        
        html = html.replace(
            "const data = await fetch('data.json').then(r => r.json());",
            f"const data = {data_json};"
        )
        
        html = html.replace(
            "import { createVisualization } from './viz.js';",
            f"/* viz.js inlined below */\n{js}"
        )
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"✅ Saved to {filename}")
