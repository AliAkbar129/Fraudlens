import React, { useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Sphere } from '@react-three/drei';
import * as THREE from 'three';

// A simple wireframe globe for now, can be enhanced with textures
const Globe = () => {
  const globeRef = useRef<THREE.Group>(null);

  useFrame(() => {
    if (globeRef.current) {
      globeRef.current.rotation.y += 0.001; // Auto-rotation
    }
  });

  return (
    <group ref={globeRef}>
      <Sphere args={[2, 64, 64]}>
        <meshBasicMaterial 
          color="#001133" 
          transparent={true} 
          opacity={0.8}
        />
      </Sphere>
      
      {/* Grid overlay */}
      <Sphere args={[2.01, 32, 32]}>
        <meshBasicMaterial 
          color="#00d4ff" 
          wireframe={true} 
          transparent={true} 
          opacity={0.15}
        />
      </Sphere>

      {/* Atmospheric glow */}
      <Sphere args={[2.2, 64, 64]}>
        <meshBasicMaterial 
          color="#00d4ff" 
          transparent={true} 
          opacity={0.05} 
          side={THREE.BackSide}
          blending={THREE.AdditiveBlending}
        />
      </Sphere>
    </group>
  );
};

// Generate random arcs for transactions
const Arcs = () => {
  const arcs = useMemo(() => {
    return Array.from({ length: 30 }).map(() => {
      const lat1 = (Math.random() - 0.5) * Math.PI;
      const lon1 = (Math.random() - 0.5) * Math.PI * 2;
      const lat2 = (Math.random() - 0.5) * Math.PI;
      const lon2 = (Math.random() - 0.5) * Math.PI * 2;
      
      const r = 2.05;
      
      const start = new THREE.Vector3(
        r * Math.cos(lat1) * Math.cos(lon1),
        r * Math.sin(lat1),
        r * Math.cos(lat1) * Math.sin(lon1)
      );
      
      const end = new THREE.Vector3(
        r * Math.cos(lat2) * Math.cos(lon2),
        r * Math.sin(lat2),
        r * Math.cos(lat2) * Math.sin(lon2)
      );

      // Control point for the bezier curve (arc)
      const mid = start.clone().lerp(end, 0.5).normalize().multiplyScalar(r * 1.5);
      
      const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
      const points = curve.getPoints(50);
      
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const isFraud = Math.random() > 0.8;
      const color = isFraud ? '#ff3366' : '#00d4ff';

      return { geometry, color, isFraud };
    });
  }, []);

  const linesRef = useRef<THREE.Group>(null);

  useEffect(() => {
    if (!linesRef.current) return;
    // Clear previous children
    while (linesRef.current.children.length > 0) {
      linesRef.current.remove(linesRef.current.children[0]);
    }
    // Add line objects imperatively to avoid JSX <line> SVG conflict
    arcs.forEach((arc) => {
      const material = new THREE.LineBasicMaterial({ color: arc.color, transparent: true, opacity: 0.6 });
      const lineObj = new THREE.Line(arc.geometry, material);
      linesRef.current!.add(lineObj);
    });
  }, [arcs]);

  useFrame(({ clock }) => {
    if (linesRef.current) {
      linesRef.current.rotation.y += 0.001; // Match globe rotation
      // Simple opacity pulsing for fraud lines
      linesRef.current.children.forEach((child: any, i: number) => {
        if (arcs[i]?.isFraud && child.material) {
          child.material.opacity = 0.5 + Math.sin(clock.elapsedTime * 5 + i) * 0.5;
        }
      });
    }
  });

  return <group ref={linesRef} />;
}

const TransactionGlobe = () => {
  return (
    <Canvas camera={{ position: [0, 0, 6], fov: 45 }} className="w-full h-full bg-[#0a0a0f]">
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#00d4ff" />
      
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
      
      <Globe />
      <Arcs />
      
      <OrbitControls 
        enablePan={false}
        enableZoom={true}
        minDistance={3}
        maxDistance={10}
        autoRotate={false}
      />
    </Canvas>
  );
};

export default TransactionGlobe;
