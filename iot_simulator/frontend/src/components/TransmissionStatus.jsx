export default function TransmissionStatus({ backendOnline, transmissionLog, countdown }) {
  const delivered = transmissionLog.filter(e => e.success).length;
  const lastTime = transmissionLog.length > 0 ? transmissionLog[0].time : null;

  return (
    <div className="transmission-status">
      <div className="status-header">
        <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`} />
        <span className="status-text">
          {backendOnline ? 'BACKEND CONNECTED' : 'BACKEND OFFLINE'}
        </span>
      </div>

      <div className="next-tx">
        Next transmission in: <strong>{countdown}s</strong>
      </div>

      {transmissionLog.length > 0 && (
        <div className="tx-log">
          <div className="tx-log-title">
            Last Transmission: {delivered}/{transmissionLog.length} delivered
            {lastTime && ` · ${lastTime.toLocaleTimeString()}`}
          </div>
          {transmissionLog.map((entry, idx) => (
            <div key={idx} className={`tx-entry ${entry.success ? 'success' : 'fail'}`}>
              <span className="tx-machine">{entry.name?.split(' ')[0] || entry.machineId?.slice(0,8)}</span>
              <span className="tx-arrow">→</span>
              <span className="tx-time">
                {entry.time.toLocaleTimeString()}
              </span>
              <span className="tx-result">
                {entry.success ? '✓' : '✗'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
