import { create } from 'zustand';
import { FraudCase } from '../types';

interface CaseState {
  cases: FraudCase[];
  selectedCase: FraudCase | null;
  filters: { status: string; priority: string; analyst: string };
  setCases: (cases: FraudCase[]) => void;
  selectCase: (c: FraudCase | null) => void;
  setFilters: (filters: any) => void;
  updateCase: (id: number, data: Partial<FraudCase>) => void;
}

export const useCaseStore = create<CaseState>((set) => ({
  cases: [],
  selectedCase: null,
  filters: { status: 'all', priority: 'all', analyst: 'all' },
  setCases: (cases) => set({ cases }),
  selectCase: (selectedCase) => set({ selectedCase }),
  setFilters: (filters) => set((state) => ({ filters: { ...state.filters, ...filters } })),
  updateCase: (id, data) => set((state) => ({
    cases: state.cases.map(c => c.id === id ? { ...c, ...data } : c),
    selectedCase: state.selectedCase?.id === id ? { ...state.selectedCase, ...data } : state.selectedCase
  }))
}));
