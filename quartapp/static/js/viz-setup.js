// Three.js Scene Setup Module - Enhanced for Colab Proxy
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
