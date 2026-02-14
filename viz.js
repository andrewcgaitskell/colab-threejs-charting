// viz.js
export function createVisualization(scene, data, THREE) {
    
    // Example: Surface
    if (data.vertices && data.resolution) {
        createSurface(scene, data, THREE);
    }
    
    // Example: Point cloud
    if (data.points) {
        createPointCloud(scene, data, THREE);
    }
}

function createSurface(scene, data, THREE) {
    const { vertices, resolution } = data;
    
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(vertices.flat());
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    // Create faces
    const indices = [];
    for (let i = 0; i < resolution - 1; i++) {
        for (let j = 0; j < resolution - 1; j++) {
            const a = i * resolution + j;
            const b = i * resolution + j + 1;
            const c = (i + 1) * resolution + j;
            const d = (i + 1) * resolution + j + 1;
            indices.push(a, c, b, b, c, d);
        }
    }
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    
    const material = new THREE.MeshPhongMaterial({
        color: data.color || 0x00ff88,
        side: THREE.DoubleSide
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
}

function createPointCloud(scene, data, THREE) {
    const { points, colors } = data;
    
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(points.flat());
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    if (colors) {
        const colorArray = new Float32Array(colors.flat());
        geometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));
    }
    
    const material = new THREE.PointsMaterial({
        size: data.pointSize || 0.05,
        vertexColors: colors ? true : false
    });
    
    const pointCloud = new THREE.Points(geometry, material);
    scene.add(pointCloud);
}
