import React, { useEffect, useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';
import * as d3 from 'd3-force-3d';
import { GraphNode, GraphEdge } from '@/types';

// Generate mock data for the force graph
const generateMockGraph = () => {
  const nodes: GraphNode[] = [];
  const links: GraphEdge[] = [];
  
  const types: GraphNode['type'][] = ['transaction', 'card', 'device', 'ip', 'email'];
  
  // Center fraud ring
  for (let i = 0; i < 50; i++) {
    nodes.push({
      id: `node-${i}`,
      type: types[Math.floor(Math.random() * types.length)],
      risk_score: Math.random() > 0.8 ? 0.9 : Math.random() * 0.4,
      label: `Node ${i}`
    });
  }

  // Create links
  for (let i = 0; i < 60; i++) {
    const source = `node-${Math.floor(Math.random() * 50)}`;
    const target = `node-${Math.floor(Math.random() * 50)}`;
    if (source !== target) {
      links.push({ source, target, type: 'connected', weight: Math.random() });
    }
  }

  return { nodes, links };
};

const ForceGraph = ({ nodes, links }: { nodes: any[], links: any[] }) => {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const linesRef = useRef<THREE.LineSegments>(null);
  
  const dummy = useMemo(() => new THREE.Object3D(), []);
  
  const colorArray = useMemo(() => {
    const colors = new Float32Array(nodes.length * 3);
    const color = new THREE.Color();
    nodes.forEach((node, i) => {
      // Map node type to color
      if (node.risk_score > 0.8) color.setHex(0xff3366);
      else if (node.type === 'transaction') color.setHex(0x00d4ff);
      else if (node.type === 'card') color.setHex(0xa855f7);
      else if (node.type === 'device') color.setHex(0x00ff88);
      else if (node.type === 'ip') color.setHex(0xffaa00);
      else color.setHex(0x475569);
      
      color.toArray(colors, i * 3);
    });
    return colors;
  }, [nodes]);

  useEffect(() => {
    // Run D3 Force simulation
    const simulation = d3.forceSimulation(nodes)
      .force('charge', d3.forceManyBody().strength(-50))
      .force('link', d3.forceLink(links).id((d: any) => d.id).distance(30))
      .force('center', d3.forceCenter(0, 0, 0))
      .stop();

    // Run physics
    for (let i = 0; i < 150; i++) simulation.tick();

    // Update positions
    if (meshRef.current) {
      nodes.forEach((node, i) => {
        dummy.position.set(node.x, node.y, node.z);
        const scale = node.risk_score > 0.8 ? 2 : 1;
        dummy.scale.set(scale, scale, scale);
        dummy.updateMatrix();
        meshRef.current!.setMatrixAt(i, dummy.matrix);
      });
      meshRef.current.instanceMatrix.needsUpdate = true;
    }

    if (linesRef.current) {
      const positions = new Float32Array(links.length * 6);
      links.forEach((link, i) => {
        positions[i * 6] = link.source.x;
        positions[i * 6 + 1] = link.source.y;
        positions[i * 6 + 2] = link.source.z;
        positions[i * 6 + 3] = link.target.x;
        positions[i * 6 + 4] = link.target.y;
        positions[i * 6 + 5] = link.target.z;
      });
      linesRef.current.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      linesRef.current.geometry.attributes.position.needsUpdate = true;
    }

  }, [nodes, links, dummy]);

  useFrame(({ clock }) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = Math.sin(clock.elapsedTime * 0.1) * 0.2;
    }
    if (linesRef.current) {
      linesRef.current.rotation.y = Math.sin(clock.elapsedTime * 0.1) * 0.2;
    }
  });

  return (
    <group>
      <instancedMesh ref={meshRef} args={[undefined, undefined, nodes.length]}>
        <sphereGeometry args={[1, 16, 16]}>
          <instancedBufferAttribute attach="attributes-color" args={[colorArray, 3]} />
        </sphereGeometry>
        <meshBasicMaterial vertexColors toneMapped={false} />
      </instancedMesh>
      
      <lineSegments ref={linesRef}>
        <bufferGeometry />
        <lineBasicMaterial color="#ffffff" transparent opacity={0.15} />
      </lineSegments>
    </group>
  );
};

const ForceGraph3D = () => {
  const data = useMemo(() => generateMockGraph(), []);

  return (
    <div className="w-full h-full relative bg-[#0a0a0f] rounded-2xl overflow-hidden border border-white/10">
      <Canvas camera={{ position: [0, 0, 150], fov: 60 }}>
        <color attach="background" args={['#0a0a0f']} />
        <ambientLight intensity={1} />
        <Stars radius={300} depth={50} count={3000} factor={4} saturation={0} fade speed={1} />
        
        <ForceGraph nodes={data.nodes} links={data.links} />
        
        <OrbitControls enablePan={true} enableZoom={true} />
      </Canvas>
      
      <div className="absolute bottom-4 left-4 flex gap-2">
        <div className="flex items-center gap-1 text-xs text-slate-400 bg-black/50 px-2 py-1 rounded-md backdrop-blur-md">
          <div className="w-2 h-2 rounded-full bg-[#00d4ff]" /> Transaction
        </div>
        <div className="flex items-center gap-1 text-xs text-slate-400 bg-black/50 px-2 py-1 rounded-md backdrop-blur-md">
          <div className="w-2 h-2 rounded-full bg-[#a855f7]" /> Card
        </div>
        <div className="flex items-center gap-1 text-xs text-slate-400 bg-black/50 px-2 py-1 rounded-md backdrop-blur-md">
          <div className="w-2 h-2 rounded-full bg-[#ff3366]" /> High Risk
        </div>
      </div>
    </div>
  );
};

export default ForceGraph3D;
