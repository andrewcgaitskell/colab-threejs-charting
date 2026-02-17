# Cell 1: Install Dependencies and Setup
## !pip install -q quart nest-asyncio

import nest_asyncio
import os
import json

nest_asyncio.apply()

# Create directory structure in current folder
base_dir = os.getcwd()  # Use current working directory
dirs = [
    f'{base_dir}/templates',
    f'{base_dir}/static/js',
    f'{base_dir}/static/css',
    f'{base_dir}/data'
]

for dir_path in dirs:
    os.makedirs(dir_path, exist_ok=True)

print('✅ Directory structure created\n')
print(f'📁 Base directory: {base_dir}')

# ============================================================================
# File 1: app.py
# ============================================================================
app_code = '''from quart import Quart, render_template, jsonify
import json
import os

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('viz.html')

@app.route('/api/data')
async def get_data():
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'test.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data) if isinstance(data, list) else 1
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'Data file not found'
        }), 404
    except json.JSONDecodeError:
        return jsonify({
            'success': False,
            'error': 'Invalid JSON format'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
'''

with open(f'{base_dir}/app.py', 'w') as f:
    f.write(app_code)
print('✅ Created: app.py')

# ============================================================================
# File 2: static/js/viz-setup.js (ENHANCED)
# ============================================================================
viz_setup_code = '''// Three.js Scene Setup Module - Enhanced for Colab Proxy
export class VizSetup {
    constructor(config = {}) {
        this.config = {
            backgroundColor: 0x0a0a0a,
            enableHelpers: true,
            enableGrid: true,
            maxPixelRatio: 2, // Cap for performance in proxy
            ...config
        };
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.resizeObserver = null;
    }

    checkWebGLSupport() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (!gl) return false;
            
            // Test basic WebGL functionality
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            if (debugInfo) {
                const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                console.log('WebGL Renderer:', renderer);
            }
            
            return true;
        } catch (e) {
            console.error('WebGL check failed:', e);
            return false;
        }
    }

    initScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(this.config.backgroundColor);
        return this.scene;
    }

    initCamera() {
        this.camera = new THREE.PerspectiveCamera(
            75, 
            window.innerWidth / window.innerHeight, 
            0.1, 
            1000
        );
        this.camera.position.set(10, 10, 10);
        return this.camera;
    }

    initRenderer(container) {
        if (!container) {
            throw new Error('Container element not found');
        }

        // Check WebGL support first
        if (!this.checkWebGLSupport()) {
            throw new Error('WebGL not supported in this environment. Try opening in a new tab or enabling hardware acceleration.');
        }

        try {
            this.renderer = new THREE.WebGLRenderer({ 
                antialias: true,
                alpha: true,
                powerPreference: 'high-performance',
                failIfMajorPerformanceCaveat: false  // Allow software rendering
            });

            // Verify context was created
            const gl = this.renderer.getContext();
            if (!gl) {
                throw new Error('WebGL context creation failed. Click "Open in New Tab" for better compatibility.');
            }

            // Cap pixel ratio for better proxy performance
            const pixelRatio = Math.min(window.devicePixelRatio, this.config.maxPixelRatio);
            this.renderer.setPixelRatio(pixelRatio);
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            
            container.appendChild(this.renderer.domElement);
            
            console.log('✅ WebGL initialized successfully');
            return this.renderer;
            
        } catch (error) {
            console.error('Renderer initialization failed:', error);
            throw new Error('Failed to initialize 3D renderer: ' + error.message);
        }
    }

    initControls(camera, renderer) {
        const OrbitControls = window.OrbitControls;
        this.controls = new OrbitControls(camera, renderer.domElement);
        
        // Optimize for proxy latency
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.1; // Increased for smoother proxy experience
        this.controls.rotateSpeed = 0.5;
        this.controls.zoomSpeed = 1.0;
        this.controls.panSpeed = 0.8;
        
        // Smoother interactions
        this.controls.minDistance = 5;
        this.controls.maxDistance = 50;
        
        return this.controls;
    }

    addLights(scene) {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
        scene.add(ambientLight);

        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 5, 5);
        scene.add(directionalLight);

        // Point light
        const pointLight = new THREE.PointLight(0x4488ff, 0.5, 50);
        pointLight.position.set(-5, -5, -5);
        scene.add(pointLight);
    }

    addHelpers(scene) {
        if (!this.config.enableHelpers) return;
        
        if (this.config.enableGrid) {
            const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
            scene.add(gridHelper);
        }

        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), wait);
        };
    }

    setupResize(camera, renderer) {
        // Use ResizeObserver for accurate container sizing
        if (typeof ResizeObserver !== 'undefined') {
            this.resizeObserver = new ResizeObserver(entries => {
                for (let entry of entries) {
                    const { width, height } = entry.contentRect;
                    
                    if (width > 0 && height > 0) {
                        camera.aspect = width / height;
                        camera.updateProjectionMatrix();
                        renderer.setSize(width, height, false);
                    }
                }
            });

            const container = renderer.domElement.parentElement;
            if (container) {
                this.resizeObserver.observe(container);
            }
        }

        // Fallback to window resize with debouncing
        const debouncedResize = this.debounce(() => {
            const width = window.innerWidth;
            const height = window.innerHeight;
            
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize(width, height);
        }, 250);

        window.addEventListener('resize', debouncedResize);
    }

    startAnimation(scene, camera, renderer, controls) {
        let frameCount = 0;
        let lastTime = performance.now();
        let fps = 60;

        function animate() {
            requestAnimationFrame(animate);
            
            // FPS monitoring (optional)
            frameCount++;
            if (frameCount % 60 === 0) {
                const currentTime = performance.now();
                const delta = currentTime - lastTime;
                fps = Math.round(60000 / delta);
                lastTime = currentTime;
                frameCount = 0;
                
                // Log performance occasionally
                if (fps < 30) {
                    console.warn('Low FPS detected:', fps);
                }
            }
            
            controls.update();
            renderer.render(scene, camera);
        }
        
        animate();
    }

    cleanup() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        if (this.renderer) {
            this.renderer.dispose();
        }
    }

    // Complete setup - convenience method
    setup(containerId) {
        const container = document.getElementById(containerId);
        
        if (!container) {
            throw new Error(`Container element #${containerId} not found`);
        }
        
        const scene = this.initScene();
        const camera = this.initCamera();
        const renderer = this.initRenderer(container);
        const controls = this.initControls(camera, renderer);
        
        this.addLights(scene);
        this.addHelpers(scene);
        this.setupResize(camera, renderer);
        
        return { scene, camera, renderer, controls };
    }
}
'''

with open(f'{base_dir}/static/js/viz-setup.js', 'w') as f:
    f.write(viz_setup_code)
print('✅ Created: static/js/viz-setup.js (Enhanced)')

# ============================================================================
# File 3: static/js/viz-data.js (WITH VALIDATION)
# ============================================================================
viz_data_code = '''// Three.js Data Visualization Module
export class VizData {
    constructor(scene) {
        if (!scene) {
            throw new Error('Scene is required for VizData');
        }
        this.scene = scene;
    }

    createPointCloud(data) {
        if (!Array.isArray(data) || data.length === 0) {
            console.warn('Invalid or empty data for point cloud');
            return null;
        }

        const geometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];

        data.forEach((point, index) => {
            positions.push(
                point.x ?? 0,
                point.y ?? 0,
                point.z ?? 0
            );

            const hue = index / data.length;
            const color = new THREE.Color().setHSL(hue, 1, 0.5);
            colors.push(color.r, color.g, color.b);
        });

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.2,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });

        const pointCloud = new THREE.Points(geometry, material);
        this.scene.add(pointCloud);
        
        console.log(`✅ Created point cloud with ${data.length} points`);
        return pointCloud;
    }

    createSpheres(data, spacing = 5) {
        if (!Array.isArray(data) || data.length === 0) {
            console.warn('Invalid or empty data for spheres');
            return [];
        }

        const spheres = [];
        let createdCount = 0;

        data.forEach((point, index) => {
            // Only create sphere every N points to avoid too many objects
            if (index % spacing !== 0) return;

            const geometry = new THREE.SphereGeometry(0.1, 16, 16);
            const hue = index / data.length;
            const material = new THREE.MeshPhongMaterial({
                color: new THREE.Color().setHSL(hue, 1, 0.5),
                emissive: new THREE.Color().setHSL(hue, 1, 0.2),
                shininess: 30
            });

            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(
                point.x ?? 0,
                point.y ?? 0,
                point.z ?? 0
            );

            this.scene.add(sphere);
            spheres.push(sphere);
            createdCount++;
        });

        console.log(`✅ Created ${createdCount} spheres (every ${spacing}th point)`);
        return spheres;
    }

    createLines(data) {
        if (!Array.isArray(data) || data.length < 2) {
            console.warn('Insufficient data for line (need at least 2 points)');
            return null;
        }

        const geometry = new THREE.BufferGeometry();
        const positions = [];

        data.forEach(point => {
            positions.push(
                point.x ?? 0,
                point.y ?? 0,
                point.z ?? 0
            );
        });

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

        const material = new THREE.LineBasicMaterial({
            color: 0x00ff00,
            linewidth: 1
        });

        const line = new THREE.Line(geometry, material);
        this.scene.add(line);
        
        console.log(`✅ Created line with ${data.length} points`);
        return line;
    }

    // Convenience method - creates visualization based on options
    visualize(data, options = {}) {
        const {
            showPoints = true,
            showSpheres = true,
            showLines = false,
            sphereSpacing = 5
        } = options;

        if (!Array.isArray(data)) {
            console.error('Data must be an array');
            return null;
        }

        const objects = {};
        let totalObjects = 0;

        if (showPoints) {
            objects.pointCloud = this.createPointCloud(data);
            if (objects.pointCloud) totalObjects++;
        }

        if (showSpheres) {
            objects.spheres = this.createSpheres(data, sphereSpacing);
            if (objects.spheres) totalObjects++;
        }

        if (showLines) {
            objects.line = this.createLines(data);
            if (objects.line) totalObjects++;
        }

        console.log(`✅ Visualization complete: ${totalObjects} object type(s) created`);
        return objects;
    }
}
'''

with open(f'{base_dir}/static/js/viz-data.js', 'w') as f:
    f.write(viz_data_code)
print('✅ Created: static/js/viz-data.js (Enhanced)')

# ============================================================================
# File 4: templates/viz.html (ENHANCED WITH ERROR HANDLING & OPEN IN TAB)
# ============================================================================
template_code = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Three.js Visualization</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div id="loading">
        <div>Loading Visualization...</div>
        <div class="spinner"></div>
        <div class="loading-hint">If stuck, try the "Open in New Tab" button</div>
    </div>
    
    <div id="error"></div>
    
    <div id="openInTab">
        <button onclick="openInNewTab()" title="Open in new tab for better WebGL compatibility">
            🔗 Open in New Tab
        </button>
    </div>
    
    <div id="info">
        <h3>Visualization</h3>
        <p>Points: <span id="pointCount">0</span></p>
        <p class="hint">💡 Drag to rotate • Scroll to zoom</p>
    </div>
    
    <div id="container"></div>
    
    <script type="importmap">
    {
        "imports": {
            "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
        }
    }
    </script>
    
    <script>
        function openInNewTab() {
            const newWindow = window.open(window.location.href, '_blank');
            if (!newWindow) {
                alert('Pop-up blocked. Please allow pop-ups and try again.');
            }
        }
    </script>
    
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        
        // Make THREE and OrbitControls globally available for modules
        window.THREE = THREE;
        window.OrbitControls = OrbitControls;
        
        // Import our custom modules
        import { VizSetup } from "{{ url_for('static', filename='js/viz-setup.js') }}";
        import { VizData } from "{{ url_for('static', filename='js/viz-data.js') }}";
        
        function showError(message, isWebGLError = false) {
            const errorDiv = document.getElementById('error');
            errorDiv.innerHTML = `
                <div class="error-content">
                    <h3>⚠️ Initialization Failed</h3>
                    <p><strong>Error:</strong> ${message}</p>
                    
                    ${isWebGLError ? `
                        <h4>Try these solutions:</h4>
                        <ol>
                            <li><strong>Click "Open in New Tab"</strong> button (top right) ✨</li>
                            <li>Enable hardware acceleration in your browser</li>
                            <li>Try Chrome if using another browser</li>
                            <li>Check WebGL status: <a href="chrome://gpu" target="_blank">chrome://gpu</a></li>
                        </ol>
                    ` : `
                        <p>Try refreshing the page or opening in a new tab.</p>
                    `}
                </div>
            `;
            errorDiv.style.display = 'block';
            document.getElementById('loading').style.display = 'none';
        }
        
        async function init() {
            try {
                console.log('🚀 Starting initialization...');
                
                // Load data
                const response = await fetch("{{ url_for('get_data') }}");
                
                if (!response.ok) {
                    throw new Error(`Failed to load data: ${response.status} ${response.statusText}`);
                }
                
                const result = await response.json();
                
                if (!result.success) {
                    throw new Error(result.error || 'Failed to load data');
                }
                
                const data = result.data;
                console.log('✅ Data loaded:', data.length, 'points');
                
                // Update UI
                document.getElementById('loading').style.display = 'none';
                document.getElementById('info').style.display = 'block';
                document.getElementById('pointCount').textContent = data.length;
                
                // Setup Three.js scene with enhanced error handling
                const vizSetup = new VizSetup({
                    backgroundColor: 0x0a0a0a,
                    enableHelpers: true,
                    enableGrid: true,
                    maxPixelRatio: 2
                });
                
                const { scene, camera, renderer, controls } = vizSetup.setup('container');
                console.log('✅ Three.js scene initialized');
                
                // Create visualization from data
                const vizData = new VizData(scene);
                vizData.visualize(data, {
                    showPoints: true,
                    showSpheres: true,
                    showLines: false,
                    sphereSpacing: 5
                });
                
                // Start animation loop
                vizSetup.startAnimation(scene, camera, renderer, controls);
                console.log('✅ Animation started');
                
                // Hide "Open in New Tab" button after successful load
                setTimeout(() => {
                    const tabButton = document.getElementById('openInTab');
                    if (tabButton) {
                        tabButton.style.opacity = '0.5';
                        tabButton.style.pointerEvents = 'auto';
                    }
                }, 2000);
                
            } catch (error) {
                console.error('❌ Initialization error:', error);
                
                const isWebGLError = error.message.toLowerCase().includes('webgl') ||
                                   error.message.toLowerCase().includes('context') ||
                                   error.message.toLowerCase().includes('renderer');
                
                showError(error.message, isWebGLError);
            }
        }
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    </script>
</body>
</html>
'''

with open(f'{base_dir}/templates/viz.html', 'w') as f:
    f.write(template_code)
print('✅ Created: templates/viz.html (Enhanced)')

# ============================================================================
# File 5: static/css/style.css (ENHANCED)
# ============================================================================
css_code = '''body { 
    margin: 0; 
    background: #000; 
    overflow: hidden;
    font-family: Arial, sans-serif;
}

#container { 
    width: 100vw; 
    height: 100vh; 
    cursor: grab;
}

#container:active {
    cursor: grabbing;
}

/* Loading */
#loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 24px;
    text-align: center;
    z-index: 1000;
}

.spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top: 4px solid white;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-hint {
    font-size: 12px;
    color: #aaa;
    margin-top: 15px;
}

/* Error Display */
#error {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(40, 40, 40, 0.95);
    color: white;
    padding: 30px;
    border-radius: 10px;
    border: 2px solid #ff6b6b;
    max-width: 600px;
    display: none;
    z-index: 1001;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.error-content h3 {
    color: #ff6b6b;
    margin: 0 0 15px 0;
}

.error-content ol {
    text-align: left;
    margin: 15px 0;
    padding-left: 20px;
}

.error-content li {
    margin: 10px 0;
}

.error-content a {
    color: #66b3ff;
}

/* Open in Tab Button */
#openInTab {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 999;
}

#openInTab button {
    background: rgba(255, 255, 255, 0.95);
    border: none;
    padding: 12px 18px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

#openInTab button:hover {
    background: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

#openInTab button:active {
    transform: translateY(0);
}

/* Info Panel */
#info {
    position: absolute;
    top: 10px;
    left: 10px;
    color: white;
    background: rgba(0, 0, 0, 0.85);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: none;
    min-width: 200px;
}

#info h3 {
    margin: 0 0 10px 0;
    font-size: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    padding-bottom: 8px;
}

#info p {
    margin: 8px 0;
    font-size: 14px;
}

#info .hint {
    font-size: 11px;
    color: #aaa;
    margin-top: 10px;
    font-style: italic;
}

/* Responsive */
@media (max-width: 768px) {
    #openInTab button {
        padding: 10px 14px;
        font-size: 12px;
    }
    
    #info {
        font-size: 12px;
        padding: 10px;
    }
    
    #error {
        max-width: 90%;
        padding: 20px;
    }
}
'''

with open(f'{base_dir}/static/css/style.css', 'w') as f:
    f.write(css_code)
print('✅ Created: static/css/style.css (Enhanced)')

# ============================================================================
# File 6: data/test.json
# ============================================================================
sample_data = [
    {"x": i/10, "y": (i**2)/100, "z": (i**1.5)/50}
    for i in range(-50, 51)
]

with open(f'{base_dir}/data/test.json', 'w') as f:
    json.dump(sample_data, f, indent=2)
print('✅ Created: data/test.json')

# ============================================================================
# File 7: requirements.txt
# ============================================================================
requirements = '''quart
'''

with open(f'{base_dir}/requirements.txt', 'w') as f:
    f.write(requirements)
print('✅ Created: requirements.txt')

# ============================================================================
# File 8: README.md (UPDATED)
# ============================================================================
readme = '''# Three.js Visualization with Quart

Production-hardened Three.js visualization running in Google Colab with Quart backend.

## Features

✅ **WebGL Error Handling** - Detects and reports WebGL issues clearly  
✅ **Proxy Optimizations** - Optimized for Colab's proxy environment  
✅ **"Open in New Tab"** - Fallback for WebGL compatibility issues  
✅ **Responsive Resize** - Uses ResizeObserver for accurate sizing  
✅ **Performance Monitoring** - FPS tracking and adaptive rendering  
✅ **Modular Architecture** - Separated setup and data visualization  

## Installation

```bash
        pip install -r requirements.txt'''

with open(f'{base_dir}/ReadMe.md', 'w') as f:
    f.write(readme)
print('✅ Created: ReadMe.md')



