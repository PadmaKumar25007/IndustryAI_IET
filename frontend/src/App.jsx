import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import Dashboard from './pages/Dashboard';
import PlaceholderPage from './pages/PlaceholderPage';
import { useSystemStatus } from './hooks/useSystemStatus';
import { NAV_ITEMS } from './config/nav';
import './App.css';

const TITLES = {
  dashboard: { title: 'Command Center', subtitle: 'Factory-wide operations at a glance' },
  employees: { title: 'Employees', subtitle: 'Workforce overview' },
  tasks: { title: 'Tasks', subtitle: 'Assignments and progress' },
  machines: { title: 'Machines', subtitle: 'Equipment and health' },
  orders: { title: 'Orders', subtitle: 'Customer demand and deadlines' },
  production: { title: 'Production', subtitle: 'Runs and output' },
  iot: { title: 'IoT Monitoring', subtitle: 'Live machine telemetry' },
  ai: { title: 'AI Assistant', subtitle: 'Administrative intelligence' },
};

export default function App() {
  const [route, setRoute] = useState('dashboard');
  const systemStatus = useSystemStatus();
  const meta = TITLES[route] || { title: NAV_ITEMS.find((n) => n.id === route)?.label || route };

  return (
    <div className="shell">
      <Sidebar active={route} onNavigate={setRoute} />
      <div className="main">
        <Topbar title={meta.title} subtitle={meta.subtitle} systemStatus={systemStatus} />
        {route === 'dashboard' ? <Dashboard /> : <PlaceholderPage page={route} />}
      </div>
    </div>
  );
}
