-- Initial Database Schema for IndAI Prototype

CREATE TABLE IF NOT EXISTS employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    skills JSONB,
    certifications JSONB,
    shift VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ACTIVE',
    availability VARCHAR(50) DEFAULT 'AVAILABLE',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS machines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    machine_type VARCHAR(100),
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'OPERATIONAL',
    health_status VARCHAR(50) DEFAULT 'GOOD',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(100) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    product VARCHAR(255),
    quantity INTEGER DEFAULT 0,
    priority VARCHAR(50) DEFAULT 'NORMAL',
    status VARCHAR(50) DEFAULT 'PENDING',
    deadline TIMESTAMPTZ,
    progress NUMERIC(5,2) DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    required_skill VARCHAR(255),
    priority VARCHAR(50) DEFAULT 'NORMAL',
    status VARCHAR(50) DEFAULT 'PENDING',
    employee_id UUID REFERENCES employees(id) ON DELETE SET NULL,
    machine_id UUID REFERENCES machines(id) ON DELETE SET NULL,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    start_time TIMESTAMPTZ,
    deadline TIMESTAMPTZ,
    progress NUMERIC(5,2) DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS production_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    machine_id UUID REFERENCES machines(id) ON DELETE SET NULL,
    quantity_target INTEGER DEFAULT 0,
    quantity_completed INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'PLANNED',
    start_time TIMESTAMPTZ,
    estimated_completion TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS machine_telemetry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL REFERENCES machines(id) ON DELETE CASCADE,
    temperature DOUBLE PRECISION,
    vibration DOUBLE PRECISION,
    current DOUBLE PRECISION,
    rpm DOUBLE PRECISION,
    machine_status VARCHAR(50),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS maintenance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL REFERENCES machines(id) ON DELETE CASCADE,
    issue VARCHAR(255) NOT NULL,
    description TEXT,
    technician VARCHAR(255),
    maintenance_date TIMESTAMPTZ,
    resolution TEXT,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID REFERENCES machines(id) ON DELETE SET NULL,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    employee_id UUID REFERENCES employees(id) ON DELETE SET NULL,
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) DEFAULT 'MEDIUM',
    description TEXT,
    status VARCHAR(50) DEFAULT 'OPEN',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS factory_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    event_type VARCHAR(100),
    description TEXT,
    machine_id UUID REFERENCES machines(id) ON DELETE SET NULL,
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    resolution_action TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ai_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_type VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    recommendation TEXT NOT NULL,
    reason TEXT,
    confidence DOUBLE PRECISION,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_tasks_employee_id ON tasks(employee_id);
CREATE INDEX IF NOT EXISTS idx_tasks_machine_id ON tasks(machine_id);
CREATE INDEX IF NOT EXISTS idx_tasks_order_id ON tasks(order_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status_priority ON tasks(status, priority);

CREATE INDEX IF NOT EXISTS idx_production_runs_order_id ON production_runs(order_id);
CREATE INDEX IF NOT EXISTS idx_production_runs_task_id ON production_runs(task_id);
CREATE INDEX IF NOT EXISTS idx_production_runs_machine_id ON production_runs(machine_id);

CREATE INDEX IF NOT EXISTS idx_telemetry_machine_id ON machine_telemetry(machine_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON machine_telemetry(timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_machine_time ON machine_telemetry(machine_id, timestamp);

CREATE INDEX IF NOT EXISTS idx_maintenance_machine_id ON maintenance(machine_id);

CREATE INDEX IF NOT EXISTS idx_incidents_machine_id ON incidents(machine_id);
CREATE INDEX IF NOT EXISTS idx_incidents_task_id ON incidents(task_id);
CREATE INDEX IF NOT EXISTS idx_incidents_employee_id ON incidents(employee_id);
CREATE INDEX IF NOT EXISTS idx_incidents_order_id ON incidents(order_id);

CREATE INDEX IF NOT EXISTS idx_factory_memory_machine_id ON factory_memory(machine_id);
CREATE INDEX IF NOT EXISTS idx_factory_memory_order_id ON factory_memory(order_id);
CREATE INDEX IF NOT EXISTS idx_factory_memory_task_id ON factory_memory(task_id);

CREATE INDEX IF NOT EXISTS idx_orders_status_deadline ON orders(status, deadline);
