// Three.js Data Visualization Module
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
