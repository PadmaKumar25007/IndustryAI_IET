const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Reusable helper for all FastAPI calls. Never scatters fetch() across
// components. Throws on HTTP errors and on timeout (Supabase cold starts
// can be slow, so the default timeout is generous).
async function request(path, { timeout = 30000 } = {}) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeout);
  try {
    const res = await fetch(`${API_BASE}${path}`, { signal: ctrl.signal });
    if (!res.ok) throw new Error(`API ${res.status} on ${path}`);
    return res.json();
  } catch (err) {
    if (err.name === 'AbortError') throw new Error(`API timeout on ${path}`);
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

// Existing backend endpoints only. No new endpoints required.
export const api = {
  health: () => request('/api/health'),
  healthDb: () => request('/api/health/db'),
  employees: () => request('/api/employees'),
  machines: () => request('/api/machines'),
  orders: () => request('/api/orders'),
  tasks: () => request('/api/tasks'),
  production: () => request('/api/production'),
  incidents: () => request('/api/incidents'),
  machineTelemetry: (machineId, limit = 20) =>
    request(`/api/machines/${machineId}/telemetry?limit=${limit}`),
};

export { API_BASE };
