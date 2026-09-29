const STATUS_META = {
  online: { dot: 'ok', label: 'SYSTEM ONLINE' },
  degraded: { dot: 'warn', label: 'API UP · DB UNREACHABLE' },
  offline: { dot: 'bad', label: 'BACKEND OFFLINE' },
  checking: { dot: 'warn', label: 'CHECKING…' },
};

export default function Topbar({ title, subtitle, systemStatus }) {
  const meta = STATUS_META[systemStatus] || STATUS_META.checking;
  return (
    <header className="topbar">
      <div className="topbar-titles">
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>
      <div className="sys-status" title="FastAPI + database health">
        <span className={`sys-dot ${meta.dot}`} aria-hidden="true" />
        <span className="sys-label">{meta.label}</span>
      </div>
    </header>
  );
}
