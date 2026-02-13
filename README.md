# Quart + Jinja2 + Three.js Charting Demo

A simple, clean demonstration of building interactive 3D visualizations using Python, Quart, Jinja2, and Three.js in Google Colab.

## Overview

This notebook shows how to:
- Generate data with **Pandas**
- Build an async web server with **Quart**
- Render templates with **Jinja2**
- Create interactive 3D charts with **Three.js**
- Make the app accessible via **ngrok**

## Quick Start

### Running in Google Colab

1. **Open the notebook in Colab:**
   - Upload `quart_threejs_demo.ipynb` to Google Colab
   - Or use: `File → Open notebook → GitHub` and enter this repository URL

2. **Run all cells** in order:
   - Cell 1: Install dependencies
   - Cell 2: Create sample data
   - Cell 3: Set up Quart app
   - Cell 4: Start ngrok tunnel
   - Cell 5: Run server
   - Cell 6: (Optional) Cleanup

3. **View the visualization:**
   - Click the public URL generated in Cell 4
   - Interact with the 3D chart:
     - **Drag** to rotate
     - **Scroll** to zoom
     - **Right-click** to pan

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
| **pyngrok** | Tunneling for Colab access |

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
4. **Ngrok Setup**: Create public tunnel
5. **Server Launch**: Run the application
6. **Cleanup**: Stop the tunnel

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
- `pyngrok` - Ngrok tunneling
- `pandas` - Data manipulation
- `numpy` - Numerical operations

No pre-installation needed in Colab!

## Notes

- The server runs continuously until interrupted
- Each run creates a new ngrok URL
- Free ngrok URLs expire after ~2 hours
- The notebook uses `nest_asyncio` to work in Colab's environment

## Troubleshooting

### Server won't start
- Make sure all cells are run in order
- Check that no other process is using port 5000

### Ngrok URL doesn't work
- Try regenerating the tunnel (re-run Cell 4)
- Check your firewall settings

### Chart doesn't display
- Ensure Three.js CDN is accessible
- Check browser console for errors
- Verify data is being passed correctly

## License

This is a demonstration project - feel free to use and modify as needed.

## Credits

Created as a simple, presentation-ready example of the Quart + Jinja2 + Three.js pattern for interactive data visualization.
