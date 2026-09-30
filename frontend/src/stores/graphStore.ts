import { create } from 'zustand';
import { GraphNode, GraphEdge } from '../types';

interface GraphState {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNode: GraphNode | null;
  physicsEnabled: boolean;
  labelsVisible: boolean;
  setGraphData: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  selectNode: (node: GraphNode | null) => void;
  togglePhysics: () => void;
  toggleLabels: () => void;
}

export const useGraphStore = create<GraphState>((set) => ({
  nodes: [],
  edges: [],
  selectedNode: null,
  physicsEnabled: true,
  labelsVisible: false,
  setGraphData: (nodes, edges) => set({ nodes, edges }),
  selectNode: (selectedNode) => set({ selectedNode }),
  togglePhysics: () => set((state) => ({ physicsEnabled: !state.physicsEnabled })),
  toggleLabels: () => set((state) => ({ labelsVisible: !state.labelsVisible })),
}));
