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
        with open('data.json', 'w') as f:
            json.dump(self.data, f)
        
        # Display
        return IFrame('viz.html', width=width, height=height)
    
    def save(self, filename='viz_export.html'):
        """Export single HTML file with embedded data"""
        with open('viz.html', 'r') as f:
            html = f.read()
        
        with open('viz.js', 'r') as f:
            js = f.read()
        
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
