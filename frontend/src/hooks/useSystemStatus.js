import { useState, useEffect } from 'react';
import { api } from '../services/api';

// Polls backend + database health for the top-bar status indicator.
// Returns: 'online' | 'degraded' | 'offline' | 'checking'
export function useSystemStatus(pollMs = 30000) {
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    let cancelled = false;

    async function check() {
      try {
        await api.health();
      } catch {
        if (!cancelled) setStatus('offline');
        return;
      }
      try {
        await api.healthDb();
        if (!cancelled) setStatus('online');
      } catch {
        if (!cancelled) setStatus('degraded');
      }
    }

    check();
    const id = setInterval(check, pollMs);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [pollMs]);

  return status;
}
