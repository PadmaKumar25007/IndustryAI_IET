import { MACHINE_STATUSES } from '../config/machines';

// Compact fleet status strip: machine counts by telemetry status plus
// backend connectivity. Driven by effective (pinned or live) statuses.
export default function FleetSummary({ machines, effectiveById, backendOnline }) {
  const counts = { RUNNING: 0, IDLE: 0, MAINTENANCE: 0, STOPPED: 0 };
  for (const m of machines) {
    const s = effectiveById[m.id]?.machine_status || 'RUNNING';
    if (s in counts) counts[s] += 1;
  }

  return (
    <div className="fleet-summary">
      <div className="fleet-stat">
        <span className="fleet-count">{machines.length}</span>
        <span className="fleet-label">Total</span>
      </div>
      {MACHINE_STATUSES.map((s) => (
        <div className="fleet-stat" key={s}>
          <span className={`fleet-count status-${s.toLowerCase()}`}>{counts[s]}</span>
          <span className="fleet-label">{s.charAt(0) + s.slice(1).toLowerCase()}</span>
        </div>
      ))}
      <div className="fleet-stat fleet-backend">
        <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`} />
        <span className="fleet-label">{backendOnline ? 'Connected' : 'Offline'}</span>
      </div>
    </div>
  );
}
