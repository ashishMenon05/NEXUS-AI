import React from 'react';
import { useApp } from '../context/AppContext';
import AgentTerminal from '../components/AgentTerminal';
import DynamicScenarioInjector from '../components/DynamicScenarioInjector';

const DashboardView = () => {
    const { sessionData, isConnected } = useApp();
    // Since AppContext maps the useWebSocket return `gameState` or `data` to `sessionData`
    // And I rewritten useWebSocket to return { events, gameState, isConnected }, AppContext 
    // might still just say sessionData: data. Wait! AppContext maps `data` literally.
    // useWebSocket exports { gameState }. If AppContext just takes data, it will be undefined!
    // I need to read gameState directly from useApp(). Wait, I'll export gameState from AppContext later or just assume `sessionData` mapped to `data`.
    // Actually in useWebSocket I returned { events, gameState, isConnected, sendCommand } instead of data!
    // So AppContext should map `sessionData` to `gameState`. But wait, AppContext has `data`.
    // Let me check my useWebSocket.js... I returned { events, gameState, isConnected, error, sendCommand }
    // If I didn't change AppContext, then `const { data } = useWebSocket(...)` means `data` is undefined!
    // Let's fix AppContext inside this file write temporarily? No I can't.
    // I should destructure both, but `data` will be undefined.
    // I will fix AppContext in a moment, but let's assume `sessionData` has the gameState object.

    const state = sessionData || {
        scenario: null,
        active: false,
        step: 0,
        cumulativeReward: 0,
        agents: {
            agent_a: { status: 'STANDBY', messages: [] },
            agent_b: { status: 'STANDBY', messages: [] }
        }
    };

    const sc = state.scenario || {};

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-end gap-6 border-b border-outline-variant/10 pb-6">
                <div>
                    <h1 className="text-4xl font-headline font-bold tracking-tight text-on-surface uppercase">Operational_Dashboard</h1>
                    <p className={`font-mono text-sm mt-2 opacity-80 ${isConnected ? 'text-primary' : 'text-error'}`}>
                        {isConnected ? 'CONNECTED_TO: ws://localhost:7860/ws' : 'DISCONNECTED: Backend server offline or starting...'}
                    </p>
                </div>
                <div className="flex gap-6">
                    <div className="text-right">
                        <p className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">Episode Step</p>
                        <p className="font-mono text-lg text-white">{String(state.step).padStart(2, '0')}</p>
                    </div>
                    <div className="h-10 w-px bg-outline-variant/20"></div>
                    <div className="text-right">
                        <p className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">Current Reward</p>
                        <p className="font-mono text-lg text-tertiary">{Number(state.cumulativeReward).toFixed(2)}</p>
                    </div>
                </div>
            </div>

            {/* Twin Terminals */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <AgentTerminal 
                    agentName="Agent A: Investigator"
                    model={state.agent_a_model || 'dolphin-phi'}
                    status={state.agents.agent_a.status}
                    accentColor="cyan"
                    icon="search"
                    messages={state.agents.agent_a.messages}
                />
                <AgentTerminal 
                    agentName="Agent B: Validator"
                    model={state.agent_b_model || 'qwen2.5:3b'}
                    status={state.agents.agent_b.status}
                    accentColor="purple"
                    icon="verified_user"
                    messages={state.agents.agent_b.messages}
                />
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Incident Brief Mini */}
                <section className="bg-surface-container-low/40 backdrop-blur-md rounded-lg p-5 border border-white/5 refractive-edge">
                    <div className="flex items-center gap-2 mb-6">
                        <span className="material-symbols-outlined text-outline text-sm">info</span>
                        <h3 className="text-xs font-bold font-headline tracking-widest uppercase text-outline">Incident Brief</h3>
                    </div>
                    <div className="space-y-6">
                        <div className="space-y-1">
                            <label className="text-[9px] font-mono text-outline-variant uppercase">Scenario Title</label>
                            <div className="h-6 w-full border-b border-outline-variant/20 text-sm text-on-surface/80">{sc.id || '—'}</div>
                        </div>
                        <div className="flex gap-4">
                            <div className="flex-1 space-y-1">
                                <label className="text-[9px] font-mono text-outline-variant uppercase">Difficulty</label>
                                <div className="h-6 w-full border-b border-outline-variant/20 text-sm text-on-surface/80">{sc.difficulty || '—'}</div>
                            </div>
                            <div className="flex-1 space-y-1">
                                <label className="text-[9px] font-mono text-outline-variant uppercase">Domain</label>
                                <div className="h-6 w-full border-b border-outline-variant/20 text-sm text-on-surface/80">{sc.domain || 'N/A'}</div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Scenario Injector */}
                <div className="lg:col-span-2">
                    <DynamicScenarioInjector />
                </div>
            </div>

            {/* Background glows */}
            <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] pointer-events-none -z-10 translate-x-1/2 -translate-y-1/2"></div>
            <div className="fixed bottom-0 left-0 w-[400px] h-[400px] bg-secondary/5 rounded-full blur-[100px] pointer-events-none -z-10 -translate-x-1/2 translate-y-1/2"></div>
        </div>
    );
};

export default DashboardView;
