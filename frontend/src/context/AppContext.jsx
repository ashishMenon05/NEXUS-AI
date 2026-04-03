import React, { createContext, useContext, useMemo } from 'react';
import useWebSocket from '../hooks/useWebSocket';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
    const { gameState, isConnected, sendCommand } = useWebSocket('ws://localhost:7860/ws');

    const value = useMemo(() => ({
        sessionData: gameState,
        isConnected,
        sendCommand
    }), [gameState, isConnected, sendCommand]);

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

export const useApp = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useApp must be used within an AppProvider');
    }
    return context;
};
