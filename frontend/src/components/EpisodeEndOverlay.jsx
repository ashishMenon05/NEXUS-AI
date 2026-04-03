import React from 'react';

const EpisodeEndOverlay = ({ isOpen, onClose, metrics }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8 animate-in fade-in duration-500">
            {/* Particle/Pulse Background */}
            <div className="absolute inset-0 bg-background/40 backdrop-blur-sm pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] opacity-10">
                    <div className="w-full h-full rounded-full border-[1px] border-primary-container/20 animate-[ping_4s_infinite]"></div>
                </div>
            </div>

            {/* Summary Modal */}
            <div className="relative w-full max-w-4xl glass-panel rounded-xl overflow-hidden shadow-[0_0_80px_rgba(0,0,0,0.8)] border border-white/10">
                {/* Modal Header */}
                <div className="flex items-center justify-between p-6 bg-surface-container-highest/20 border-b border-white/5">
                    <div className="flex items-center gap-3">
                        <div className="p-1 rounded bg-primary-container/20 border border-primary-container/40">
                            <span className="text-primary material-symbols-outlined text-xl">task_alt</span>
                        </div>
                        <h2 className="font-headline font-bold text-lg tracking-widest text-on-surface uppercase">Episode_Execution_Complete</h2>
                    </div>
                    <button onClick={onClose} className="text-outline hover:text-white transition-colors">
                        <span className="material-symbols-outlined">close</span>
                    </button>
                </div>

                <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-12">
                    {/* Left Column: Primary Metrics */}
                    <div className="space-y-10">
                        <div className="space-y-2">
                            <span className="font-mono text-[10px] text-outline tracking-widest uppercase">Cumulative Efficiency Score</span>
                            <div className="flex items-baseline gap-2">
                                <span className="font-headline text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-br from-primary to-primary-container drop-shadow-[0_0_15px_rgba(0,212,255,0.3)]">
                                    {metrics?.score || '—'}
                                </span>
                                <span className="font-headline text-2xl text-primary/40 font-light">pts</span>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-surface-container-lowest/50 p-4 border-l border-primary/20 refractive-edge">
                                <span className="font-mono text-[9px] text-outline uppercase block mb-1">Total Runtime</span>
                                <span className="font-headline text-2xl font-medium">{metrics?.runtime || '—'}</span>
                            </div>
                            <div className="bg-surface-container-lowest/50 p-4 border-l border-primary/20 refractive-edge">
                                <span className="font-mono text-[9px] text-outline uppercase block mb-1">Steps Executed</span>
                                <span className="font-headline text-2xl font-medium">{metrics?.steps || '—'}</span>
                            </div>
                        </div>
                        <div className="flex items-center gap-4 p-5 bg-tertiary/5 border border-tertiary/10 rounded-lg">
                            <div className="p-3 rounded-full bg-tertiary/10 text-tertiary">
                                <span className="material-symbols-outlined">troubleshoot</span>
                            </div>
                            <div>
                                <span className="font-mono text-[10px] text-tertiary/60 uppercase block">Terminal Analysis</span>
                                <span className="text-sm font-medium tracking-wide">Root Cause Found: <span className="font-mono text-tertiary">{metrics?.rootCause || '—'}</span></span>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Agent Metrics */}
                    <div className="space-y-6">
                        <h3 className="font-mono text-[10px] text-outline tracking-widest uppercase mb-4">Agent Performance Breakdown</h3>
                        {/* Agent A */}
                        <div className="relative group">
                            <div className="absolute -left-4 top-0 bottom-0 w-1 bg-primary shadow-[0_0_8px_rgba(0,212,255,0.4)]"></div>
                            <div className="bg-surface-container-low/40 p-5 space-y-4 border border-white/5 rounded-r-lg">
                                <div className="flex justify-between items-center">
                                    <span className="font-headline font-bold text-primary tracking-tighter uppercase">Agent_Alpha</span>
                                    <span className="font-mono text-[10px] text-primary/50">CYAN_PROTOCOL</span>
                                </div>
                                <div className="grid grid-cols-3 gap-2 text-center">
                                    <div>
                                        <span className="font-mono text-[9px] text-outline block uppercase">ACCURACY</span>
                                        <span className="font-headline text-lg font-medium text-primary">{metrics?.agentA?.accuracy || '—'}</span>
                                    </div>
                                    <div className="border-x border-white/5">
                                        <span className="font-mono text-[9px] text-outline block uppercase">LATENCY</span>
                                        <span className="font-headline text-lg font-medium text-primary">{metrics?.agentA?.latency || '—'}</span>
                                    </div>
                                    <div>
                                        <span className="font-mono text-[9px] text-outline block uppercase">IOPS</span>
                                        <span className="font-headline text-lg font-medium text-primary">{metrics?.agentA?.iops || '—'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {/* Agent B */}
                        <div className="relative group">
                            <div className="absolute -left-4 top-0 bottom-0 w-1 bg-secondary shadow-[0_0_8px_rgba(221,183,255,0.4)]"></div>
                            <div className="bg-surface-container-low/40 p-5 space-y-4 border border-white/5 rounded-r-lg">
                                <div className="flex justify-between items-center">
                                    <span className="font-headline font-bold text-secondary tracking-tighter uppercase">Agent_Bravo</span>
                                    <span className="font-mono text-[10px] text-secondary/50">VIOLET_PROTOCOL</span>
                                </div>
                                <div className="grid grid-cols-3 gap-2 text-center">
                                    <div>
                                        <span className="font-mono text-[9px] text-outline block uppercase">ACCURACY</span>
                                        <span className="font-headline text-lg font-medium text-secondary">{metrics?.agentB?.accuracy || '—'}</span>
                                    </div>
                                    <div className="border-x border-white/5">
                                        <span className="font-mono text-[9px] text-outline block uppercase">LATENCY</span>
                                        <span className="font-headline text-lg font-medium text-secondary">{metrics?.agentB?.latency || '—'}</span>
                                    </div>
                                    <div>
                                        <span className="font-mono text-[9px] text-outline block uppercase">IOPS</span>
                                        <span className="font-headline text-lg font-medium text-secondary">{metrics?.agentB?.iops || '—'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Modal Footer */}
                <div className="p-6 bg-surface-container-lowest/90 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="flex items-center gap-2 text-outline/40">
                        <span className="material-symbols-outlined text-sm">info</span>
                        <span className="font-mono text-[9px] uppercase tracking-wider">Session telemetry encrypted and cached locally</span>
                    </div>
                    <div className="flex gap-4 w-full md:w-auto">
                        <button className="flex-1 md:flex-none px-8 py-2.5 bg-transparent border border-outline-variant/30 text-on-surface hover:bg-white/5 transition-all font-mono text-xs tracking-widest uppercase">
                            Export Log
                        </button>
                        <button onClick={onClose} className="flex-1 md:flex-none px-12 py-2.5 bg-primary/20 border border-primary text-primary hover:bg-primary/30 transition-all font-mono text-xs tracking-widest font-bold uppercase shadow-[0_0_20px_rgba(0,212,255,0.1)]">
                            Dismiss
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EpisodeEndOverlay;
