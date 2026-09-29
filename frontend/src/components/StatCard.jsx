export default function StatCard({ label, value, sub, loading }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className="stat-value">{loading ? '—' : value}</div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  );
}
