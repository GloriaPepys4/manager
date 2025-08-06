# 部署指南

## Vercel 部署

### 前置要求
- Vercel 账号
- GitHub 账号
- Supabase 账号

### 部署步骤

#### 1. 准备 Supabase 数据库

1. 登录 [Supabase](https://supabase.com)
2. 创建新项目
3. 在 SQL 编辑器中执行 `backend/migrations/001_initial_schema.sql`
4. 记录以下信息：
   - Project URL
   - Anon Key
   - Service Key

#### 2. 配置环境变量

在 Vercel 项目设置中添加以下环境变量：

```env
SUPABASE_URL=你的Supabase项目URL
SUPABASE_ANON_KEY=你的Anon Key
SUPABASE_SERVICE_KEY=你的Service Key
SECRET_KEY=生成一个随机密钥
JWT_SECRET_KEY=生成另一个随机密钥
```

#### 3. 部署到 Vercel

```bash
# 安装 Vercel CLI
npm i -g vercel

# 在项目根目录执行
vercel

# 按照提示配置项目
```

或者通过 GitHub 集成：

1. 将项目推送到 GitHub
2. 在 Vercel 控制台导入 GitHub 项目
3. 使用 `deploy/vercel/vercel.json` 作为配置文件

## 本地开发环境

### 使用 Docker

```bash
# 构建镜像
docker build -t data-platform .

# 运行容器
docker run -p 5000:5000 -p 5173:5173 data-platform
```

### 手动部署

#### 前端部署

```bash
cd frontend
npm install
npm run build
# 将 dist 目录部署到静态服务器
```

#### 后端部署

```bash
cd backend
pip install -r requirements.txt

# 使用 Gunicorn 运行
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 生产环境配置

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL 配置

使用 Let's Encrypt 获取免费 SSL 证书：

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

## 监控和日志

### 日志配置

在 `backend/config/settings.py` 中配置日志：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/data-platform/app.log',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### 性能监控

推荐使用以下工具：
- **New Relic**: 应用性能监控
- **Sentry**: 错误追踪
- **Prometheus + Grafana**: 系统监控

## 备份策略

### 数据库备份

```bash
# PostgreSQL 备份
pg_dump -U username -d database_name > backup.sql

# 恢复
psql -U username -d database_name < backup.sql
```

### 定时备份脚本

```bash
#!/bin/bash
# 每日备份脚本
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U username -d database_name > /backup/db_$DATE.sql
find /backup -name "db_*.sql" -mtime +7 -delete
```

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查环境变量配置
   - 确认数据库服务正常运行
   - 检查防火墙设置

2. **API 响应慢**
   - 检查数据库查询性能
   - 增加缓存层
   - 优化索引

3. **前端白屏**
   - 检查 API 地址配置
   - 查看浏览器控制台错误
   - 确认静态资源正确加载

## 扩展和优化

### 性能优化建议

1. **使用 Redis 缓存**
```python
import redis
cache = redis.Redis(host='localhost', port=6379, db=0)
```

2. **启用 Gzip 压缩**
```python
from flask_compress import Compress
Compress(app)
```

3. **数据库连接池**
```python
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_RECYCLE = 3600
```

### 安全加固

1. 启用 HTTPS
2. 实施速率限制
3. 定期更新依赖
4. 使用环境变量管理敏感信息
5. 实施 CORS 策略

## 联系支持

部署遇到问题？请联系技术团队。
