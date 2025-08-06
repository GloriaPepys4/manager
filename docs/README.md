# 数据整合平台 - 项目说明文档

## 📋 项目概述

**数据整合平台**是一个企业级的前后端分离项目，用于整合11个外部充电平台的数据，提供统一的数据管理、处理和结算功能。

- **解决的问题**：多平台数据格式不统一，手工处理效率低
- **目标用户**：企业数据管理人员、财务结算人员
- **核心价值**：自动化数据处理，提高结算准确性

## 🏗️ 项目架构

### 整体架构
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   前端应用   │────▶│   API网关    │────▶│   数据库    │
│  Vue 3 + TS │     │  Flask API  │     │  Supabase   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 目录结构
```
D:\Desktop\manager\
├── frontend/              # Vue 3 前端应用
│   ├── src/              
│   │   ├── assets/       # 静态资源
│   │   ├── components/   # 通用组件
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # Pinia状态管理
│   │   ├── utils/        # 工具函数
│   │   └── views/        # 页面组件
│   ├── package.json      # 前端依赖
│   └── vite.config.ts    # Vite配置
│
├── api/                   # Vercel部署的API服务
│   ├── index.py          # Flask API入口
│   └── requirements.txt  # Python依赖
│
├── backend/              # 本地开发后端（SQLite版）
│   ├── app.py           # Flask应用
│   └── instance/        # SQLite数据库
│
├── supabase/            # 数据库配置
│   └── migrations/      # 数据库迁移脚本
│       └── 001_initial_schema.sql
│
├── .trae/               # 项目文档
│   └── documents/       
│       ├── 数据整合平台-产品需求文档.md
│       └── 数据整合平台-技术架构文档.md
│
├── vercel.json          # Vercel部署配置
├── .env.example         # 环境变量示例
└── requirements.txt     # 根目录Python依赖
```

## 🛠 技术栈

### 前端技术
- **框架**: Vue 3.5 + TypeScript 5.8
- **UI组件**: Element Plus 2.10
- **状态管理**: Pinia 3.0
- **路由**: Vue Router 4.5
- **HTTP客户端**: Axios 1.11
- **构建工具**: Vite 7.0
- **代码规范**: ESLint + Prettier

### 后端技术
- **框架**: Flask 2.3
- **数据库**: Supabase (PostgreSQL)
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (PyJWT)
- **密码加密**: Werkzeug Security
- **跨域**: Flask-CORS
- **部署**: Vercel Functions

### 数据库
- **生产环境**: Supabase PostgreSQL
- **开发环境**: SQLite
- **数据处理**: Pandas + OpenPyXL

## 💼 功能模块

### 用户角色
| 角色 | 权限 | 说明 |
|------|------|------|
| 管理员 | 全部权限 | 系统配置、用户管理 |
| 数据操作员 | 数据管理 | 数据导入、查询、修改 |
| 财务人员 | 财务功能 | 对账、结算、账单导出 |

### 核心功能
1. **用户认证** - JWT令牌认证，角色权限管理
2. **车队管理** - 车队信息维护，计价规则配置
3. **车辆管理** - 车辆信息管理，司机信息维护
4. **站点管理** - 充电站点信息管理
5. **订单管理** - 11个平台订单数据整合
6. **充值管理** - 充值记录导入与查询
7. **数据导入** - 多平台数据自动化导入
8. **数据导出** - 条件查询与批量导出
9. **对账中心** - 月度结算，余额管理
10. **系统设置** - 用户管理，系统配置

## 🚀 快速开始

### 环境要求
- Node.js >= 20.19.0
- Python >= 3.8
- MySQL 8.0 或 PostgreSQL

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:5173
```

### 后端启动

#### 方式1：使用Vercel API（推荐）

```bash
# 进入API目录
cd api

# 创建环境变量文件
cp ../.env.example .env

# 编辑.env文件，配置以下变量：
# SUPABASE_URL=你的Supabase项目URL
# SUPABASE_ANON_KEY=你的Supabase匿名密钥
# SUPABASE_SERVICE_KEY=你的Supabase服务密钥
# SECRET_KEY=你的Flask密钥
# JWT_SECRET_KEY=你的JWT密钥

# 安装依赖
pip install -r requirements.txt

# 运行API服务
python index.py
```

#### 方式2：使用本地SQLite版本

```bash
# 进入backend目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# API服务运行在 http://localhost:5000
```

### 数据库初始化

如果使用Supabase：
1. 创建Supabase项目
2. 在SQL编辑器中执行 `supabase/migrations/001_initial_schema.sql`
3. 配置环境变量

如果使用本地数据库：
- SQLite会自动创建
- 默认管理员账号：admin/admin123

## 📝 API文档

### 认证接口

#### 登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### 注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "role": "operator"
}
```

### 数据管理接口

#### 获取车辆列表
```http
GET /api/vehicles?page=1&per_page=20
Authorization: Bearer {token}
```

#### 导入订单数据
```http
POST /api/orders/import
Authorization: Bearer {token}
Content-Type: multipart/form-data

platform_id: 1
file: [Excel文件]
```

## 🔧 配置说明

### 环境变量配置

创建 `.env` 文件：

```env
# Supabase配置
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# 应用配置
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=jwt-secret-string

# 数据库配置（本地开发）
DATABASE_URL=sqlite:///data_platform.db
```

### Vercel部署配置

`vercel.json` 已配置好：
- 前端自动构建部署
- API函数自动部署
- 环境变量自动注入

## 📊 数据模型

### 核心数据表

1. **users** - 用户表
2. **fleets** - 车队表
3. **vehicles** - 车辆表
4. **stations** - 站点表
5. **orders** - 订单表
6. **platform_raw_data** - 平台原始数据
7. **recharge_records** - 充值记录
8. **fleet_balance** - 车队余额
9. **pricing_rules** - 计价规则
10. **discount_rules** - 优惠规则

## 🔐 安全注意事项

⚠️ **重要提醒**：
1. 项目中的API密钥需要更换为您自己的
2. 生产环境部署前必须修改所有默认密码
3. 建议启用HTTPS
4. 定期备份数据库

## 📈 性能优化建议

1. **前端优化**
   - 使用路由懒加载
   - 组件按需引入
   - 图片懒加载

2. **后端优化**
   - 使用Redis缓存
   - 数据库查询优化
   - 批量操作优化

3. **部署优化**
   - 使用CDN加速
   - 启用Gzip压缩
   - 数据库连接池

## 🤝 开发团队

- 产品设计：产品团队
- 前端开发：前端团队
- 后端开发：后端团队
- 测试支持：QA团队

## 📄 许可证

本项目为企业内部项目，未经授权禁止外部使用。

## 📞 联系支持

如有问题，请联系技术支持团队。

---

*最后更新：2025年1月6日*
