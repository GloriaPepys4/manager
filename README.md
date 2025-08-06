# 数据整合平台

一个企业级的前后端分离项目，用于整合11个外部充电平台的数据。

## 🚀 快速开始

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 📁 项目结构

```
manager/
├── frontend/          # Vue 3 前端应用
├── backend/           # Flask 后端应用
├── deploy/           # 部署配置
├── docs/             # 项目文档
├── scripts/          # 工具脚本
└── tests/            # 测试文件
```

## 📖 详细文档

- [项目完整说明](./docs/README.md)
- [产品需求文档](./docs/requirements/PRD.md)
- [技术架构文档](./docs/requirements/TECH.md)
- [API文档](./docs/API.md)
- [部署指南](./docs/DEPLOY.md)

## 🔧 技术栈

- **前端**: Vue 3 + TypeScript + Element Plus
- **后端**: Flask + SQLAlchemy + JWT
- **数据库**: Supabase (PostgreSQL) / SQLite (开发)
- **部署**: Vercel

## 📄 许可证

企业内部项目，未经授权禁止外部使用。
