// Health assessment of pinned sensor values against a baseline.
// Live (unpinned) machines report exact baseline values, so they stay GOOD.
export function assessHealth(baseline, values) {
  const base = baseline || { temperature: 60, vibration: 2, current: 8 };
  const tempRise = (values.temperature ?? base.temperature) - base.temperature;
  const vibRatio = (values.vibration ?? base.vibration) / Math.max(base.vibration, 0.1);
  const curRatio = (values.current ?? base.current) / Math.max(base.current, 0.1);

  if (tempRise >= 20 || vibRatio >= 2.5 || curRatio >= 1.5) return 'CRITICAL';
  if (tempRise >= 10 || vibRatio >= 1.8 || curRatio >= 1.25) return 'WARNING';
  return 'GOOD';
}

export const HEALTH_COLORS = {
  GOOD: '#22c55e',
  WARNING: '#eab308',
  CRITICAL: '#ef4444',
};
