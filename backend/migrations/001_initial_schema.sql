-- 数据整合平台 - 初始数据库架构
-- 创建时间: 2025-01-06

-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建用户表 (users)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'operator' CHECK (role IN ('admin', 'operator', 'finance')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建车队表 (fleets)
CREATE TABLE fleets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(50),
    phone VARCHAR(20),
    address TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建站点表 (stations)
CREATE TABLE stations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    address TEXT,
    region VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
    charging_piles INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建车辆表 (vehicles)
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    fleet_id UUID REFERENCES fleets(id) ON DELETE CASCADE,
    vehicle_type VARCHAR(50),
    driver_name VARCHAR(50),
    driver_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
    remark TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建订单表 (orders)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_no VARCHAR(50) UNIQUE NOT NULL,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    station_id UUID REFERENCES stations(id) ON DELETE SET NULL,
    platform_id INTEGER NOT NULL CHECK (platform_id BETWEEN 1 AND 11),
    amount DECIMAL(10,2) NOT NULL,
    settlement_amount DECIMAL(10,2),
    order_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建平台原始数据表 (platform_raw_data)
CREATE TABLE platform_raw_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform_id INTEGER NOT NULL CHECK (platform_id BETWEEN 1 AND 11),
    raw_data JSONB NOT NULL,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    imported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建充值记录表 (recharge_records)
CREATE TABLE recharge_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fleet_id UUID REFERENCES fleets(id) ON DELETE CASCADE,
    amount DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(50),
    recharge_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed')),
    remark TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建车队余额表 (fleet_balance)
CREATE TABLE fleet_balance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fleet_id UUID REFERENCES fleets(id) ON DELETE CASCADE,
    previous_balance DECIMAL(12,2) DEFAULT 0.00,
    monthly_consumption DECIMAL(12,2) DEFAULT 0.00,
    monthly_recharge DECIMAL(12,2) DEFAULT 0.00,
    current_balance DECIMAL(12,2) DEFAULT 0.00,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(fleet_id, year, month)
);

-- 创建车队余额历史表 (fleet_balance_history)
CREATE TABLE fleet_balance_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fleet_id UUID REFERENCES fleets(id) ON DELETE CASCADE,
    previous_balance DECIMAL(12,2) DEFAULT 0.00,
    monthly_consumption DECIMAL(12,2) DEFAULT 0.00,
    monthly_recharge DECIMAL(12,2) DEFAULT 0.00,
    current_balance DECIMAL(12,2) DEFAULT 0.00,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    settled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建计价规则表 (pricing_rules)
CREATE TABLE pricing_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fleet_id UUID REFERENCES fleets(id) ON DELETE CASCADE,
    time_period VARCHAR(50) NOT NULL,
    price_per_kwh DECIMAL(8,4) NOT NULL,
    effective_date DATE NOT NULL,
    expiry_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建优惠规则表 (discount_rules)
CREATE TABLE discount_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fleet_id UUID REFERENCES fleets(id) ON DELETE CASCADE,
    rule_type VARCHAR(50) NOT NULL,
    discount_rate DECIMAL(5,4) NOT NULL CHECK (discount_rate BETWEEN 0 AND 1),
    min_amount DECIMAL(10,2) DEFAULT 0.00,
    effective_date DATE NOT NULL,
    expiry_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

CREATE INDEX idx_fleets_name ON fleets(name);
CREATE INDEX idx_fleets_status ON fleets(status);

CREATE INDEX idx_stations_name ON stations(name);
CREATE INDEX idx_stations_region ON stations(region);
CREATE INDEX idx_stations_status ON stations(status);

CREATE INDEX idx_vehicles_license_plate ON vehicles(license_plate);
CREATE INDEX idx_vehicles_fleet_id ON vehicles(fleet_id);
CREATE INDEX idx_vehicles_status ON vehicles(status);

CREATE INDEX idx_orders_order_no ON orders(order_no);
CREATE INDEX idx_orders_vehicle_id ON orders(vehicle_id);
CREATE INDEX idx_orders_station_id ON orders(station_id);
CREATE INDEX idx_orders_platform_id ON orders(platform_id);
CREATE INDEX idx_orders_order_time ON orders(order_time);
CREATE INDEX idx_orders_status ON orders(status);

CREATE INDEX idx_platform_raw_data_platform_id ON platform_raw_data(platform_id);
CREATE INDEX idx_platform_raw_data_order_id ON platform_raw_data(order_id);

CREATE INDEX idx_recharge_records_fleet_id ON recharge_records(fleet_id);
CREATE INDEX idx_recharge_records_recharge_time ON recharge_records(recharge_time);
CREATE INDEX idx_recharge_records_status ON recharge_records(status);

CREATE INDEX idx_fleet_balance_fleet_id ON fleet_balance(fleet_id);
CREATE INDEX idx_fleet_balance_year_month ON fleet_balance(year, month);

CREATE INDEX idx_fleet_balance_history_fleet_id ON fleet_balance_history(fleet_id);
CREATE INDEX idx_fleet_balance_history_year_month ON fleet_balance_history(year, month);

CREATE INDEX idx_pricing_rules_fleet_id ON pricing_rules(fleet_id);
CREATE INDEX idx_pricing_rules_effective_date ON pricing_rules(effective_date);

CREATE INDEX idx_discount_rules_fleet_id ON discount_rules(fleet_id);
CREATE INDEX idx_discount_rules_effective_date ON discount_rules(effective_date);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要的表添加更新时间触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_fleets_updated_at BEFORE UPDATE ON fleets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_stations_updated_at BEFORE UPDATE ON stations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_fleet_balance_updated_at BEFORE UPDATE ON fleet_balance FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入初始数据
-- 创建默认管理员用户
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uDu2', 'admin'),
('operator1', 'operator1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uDu2', 'operator'),
('finance1', 'finance1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uDu2', 'finance');

-- 创建示例车队
INSERT INTO fleets (name, contact_person, phone, address) VALUES 
('示例车队A', '张三', '13800138001', '北京市朝阳区示例地址1号'),
('示例车队B', '李四', '13800138002', '上海市浦东新区示例地址2号'),
('示例车队C', '王五', '13800138003', '广州市天河区示例地址3号');

-- 创建示例站点
INSERT INTO stations (name, address, region, charging_piles) VALUES 
('北京示例充电站1', '北京市朝阳区充电站地址1', '北京', 10),
('北京示例充电站2', '北京市海淀区充电站地址2', '北京', 8),
('上海示例充电站1', '上海市浦东新区充电站地址1', '上海', 12),
('广州示例充电站1', '广州市天河区充电站地址1', '广州', 6);

-- 启用行级安全策略 (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE fleets ENABLE ROW LEVEL SECURITY;
ALTER TABLE stations ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform_raw_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE recharge_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE fleet_balance ENABLE ROW LEVEL SECURITY;
ALTER TABLE fleet_balance_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE pricing_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE discount_rules ENABLE ROW LEVEL SECURITY;

-- 创建基本的RLS策略（允许认证用户访问）
CREATE POLICY "Allow authenticated users to view all data" ON users FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON fleets FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON stations FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON vehicles FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON orders FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON platform_raw_data FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON recharge_records FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON fleet_balance FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON fleet_balance_history FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON pricing_rules FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to view all data" ON discount_rules FOR SELECT USING (auth.role() = 'authenticated');

-- 创建插入、更新、删除策略（允许认证用户操作）
CREATE POLICY "Allow authenticated users to insert" ON fleets FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to update" ON fleets FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to delete" ON fleets FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to insert" ON stations FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to update" ON stations FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to delete" ON stations FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to insert" ON vehicles FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to update" ON vehicles FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to delete" ON vehicles FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to insert" ON orders FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to update" ON orders FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to delete" ON orders FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to insert" ON recharge_records FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to update" ON recharge_records FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to delete" ON recharge_records FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to insert" ON fleet_balance FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to update" ON fleet_balance FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow authenticated users to delete" ON fleet_balance FOR DELETE USING (auth.role() = 'authenticated');

-- 注释
COMMENT ON TABLE users IS '用户表 - 存储系统用户信息';
COMMENT ON TABLE fleets IS '车队表 - 存储车队基本信息';
COMMENT ON TABLE stations IS '站点表 - 存储充电站点信息';
COMMENT ON TABLE vehicles IS '车辆表 - 存储车辆信息';
COMMENT ON TABLE orders IS '订单表 - 存储充电订单信息';
COMMENT ON TABLE platform_raw_data IS '平台原始数据表 - 存储各平台的原始数据';
COMMENT ON TABLE recharge_records IS '充值记录表 - 存储车队充值记录';
COMMENT ON TABLE fleet_balance IS '车队余额表 - 存储车队当前余额信息';
COMMENT ON TABLE fleet_balance_history IS '车队余额历史表 - 存储车队历史结算记录';
COMMENT ON TABLE pricing_rules IS '计价规则表 - 存储车队计价规则';
COMMENT ON TABLE discount_rules IS '优惠规则表 - 存储车队优惠规则';