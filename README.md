# Quart + Jinja2 + Three.js Charting Demo

[![Open In Colab - Quart](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/andrewcgaitskell/colab-threejs-charting/blob/main/quart_threejs_demo.ipynb)
[![Open In Colab - Simple](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/andrewcgaitskell/colab-threejs-charting/blob/main/simple_threejs_demo.ipynb)

A demonstration of building interactive 3D visualizations using Python and Three.js in Google Colab with two different approaches.

![Preview](https://github.com/user-attachments/assets/9e94b02c-978f-4bbf-893f-31cebcf342b6)

*Interactive 3D bar chart showing quarterly sales data*

## Overview

This repository provides two approaches for creating interactive 3D visualizations using Three.js in Google Colab.

## Two Approaches

This repository now offers two ways to create Three.js visualizations in Colab:

### 1. **Quart Server Approach** (Original)
- Uses Quart web server + Jinja2 templates
- Great for complex dashboards and multi-page apps
- Requires server setup
- See: `quart_threejs_demo.ipynb`

### 2. **Simple Direct Approach** (New)
- No server required - pure HTML/JS
- Minimal setup, secure data passing
- Perfect for quick visualizations
- See: `simple_threejs_demo.ipynb`

Quick comparison:

| Feature | Quart Approach | Simple Approach |
|---------|---------------|-----------------|
| Setup | Install Quart, run server | Import viz.py |
| Use Case | Dashboards, complex apps | Quick visualizations |
| Files Generated | Templates + server | Single HTML file |
| Data Passing | Jinja2 templating | JSON + secure validation |
| Security | Template-based | Data/code separation |

Choose based on your needs:
- **Quick 3D plots?** → Use Simple Approach
- **Full dashboard?** → Use Quart Approach

## Quart Approach Overview

The Quart approach shows how to:
- Generate data with **Pandas**
- Build an async web server with **Quart**
- Render templates with **Jinja2**
- Create interactive 3D charts with **Three.js**

## Quick Start

### Running in Google Colab

1. **Open the notebook in Colab:**
   - Go to [Google Colab](https://colab.research.google.com/)
   - Upload `quart_threejs_demo.ipynb` to Google Colab
   - Or use: `File → Open notebook → GitHub` and paste this repository URL

2. **Run all cells** in order (Runtime → Run all, or Ctrl+F9):
   - Cell 1: Install dependencies (takes ~30 seconds)
   - Cell 2: Create sample data
   - Cell 3: Set up Quart app
   - Cell 4: Run server (keeps running)

3. **View the visualization:**
   - The server runs on localhost:5000
   - In Google Colab, you can use port forwarding or other tools to access the local server
   - Interact with the 3D chart:
     - **Drag** to rotate the view
     - **Scroll** to zoom in/out
     - **Right-click** to pan (if needed)

### Example Output

When you run the notebook, you'll see:
- A 3D bar chart with 16 bars (4 products × 4 quarters)
- Each product has a different color (Blue, Red, Green, Orange)
- Interactive controls for exploring the data
- Grid and axes for orientation

## What You'll See

A 3D bar chart showing quarterly sales data for four products:
- Product A (Blue)
- Product B (Red)
- Product C (Green)
- Product D (Orange)

Each bar represents sales volume for a specific product in a specific quarter (Q1-Q4).

## Technology Stack

| Component | Purpose |
|-----------|---------|
| **Quart** | Async Python web framework (Flask-like API) |
| **Jinja2** | HTML templating engine |
| **Three.js** | 3D graphics library for WebGL |
| **Pandas** | Data manipulation |

## Data Flow

```
Pandas DataFrame
    ↓
Python Dictionary
    ↓
Jinja2 Template (JSON conversion)
    ↓
JavaScript (Three.js)
    ↓
Interactive 3D Visualization
```

## Code Structure

The notebook is organized into clear sections:

1. **Dependencies**: Install required packages
2. **Data Creation**: Generate sample data with Pandas
3. **Quart App**: Define routes and Jinja2 template
4. **Server Launch**: Run the application

## Customization

### Change the Data

Modify the data in Cell 2:

```python
data = {
    'Product': ['Your Products'],
    'Q1': [your_values],
    # ... more quarters
}
```

### Modify Chart Appearance

In Cell 3, update the Three.js code:
- Colors: Change the `colors` array
- Size: Adjust bar geometry dimensions
- Layout: Modify position calculations

### Add More Features

The template is designed to be extended:
- Add chart labels
- Include legends
- Add animations
- Implement tooltips
- Create multiple chart types

## Use Cases

This pattern is ideal for:

- **Executive Dashboards**: Present data insights to management
- **Prototyping**: Quick visualization of data concepts
- **Education**: Teaching web development and data visualization
- **Research**: Exploring 3D data representations
- **Presentations**: Creating interactive demonstrations

## Requirements

The notebook automatically installs these packages:
- `quart` - Async web framework
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `requests` - HTTP library for loading templates

No pre-installation needed in Colab!

## Notes

- The server runs continuously until interrupted
- The server runs on localhost:5000
- In Google Colab, you may need to use port forwarding to access localhost

## Troubleshooting

### Server won't start
- Make sure all cells are run in order
- Check that no other process is using port 5000

### Chart doesn't display
- Ensure Three.js CDN is accessible
- Check browser console for errors
- Verify data is being passed correctly

## License

This is a demonstration project - feel free to use and modify as needed.

## Credits

Created as a simple, presentation-ready example of the Quart + Jinja2 + Three.js pattern for interactive data visualization.
