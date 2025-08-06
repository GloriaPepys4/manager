# API 文档

## 基础信息

- **基础URL**: `http://localhost:5000/api` (开发环境)
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

## 认证相关

### 用户登录

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJ...",
    "user": {
      "id": "uuid",
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin"
    }
  }
}
```

### 用户注册

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "operator"
}
```

## 车辆管理

### 获取车辆列表

```http
GET /api/vehicles?page=1&per_page=20&keyword=search
Authorization: Bearer {token}
```

**查询参数**
- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 20)
- `keyword`: 搜索关键词

### 创建车辆

```http
POST /api/vehicles
Authorization: Bearer {token}
Content-Type: application/json

{
  "license_plate": "string",
  "fleet_id": "uuid",
  "vehicle_type": "string",
  "driver_name": "string",
  "driver_phone": "string"
}
```

### 更新车辆

```http
PUT /api/vehicles/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "license_plate": "string",
  "vehicle_type": "string",
  "status": "active"
}
```

### 删除车辆

```http
DELETE /api/vehicles/{id}
Authorization: Bearer {token}
```

## 车队管理

### 获取车队列表

```http
GET /api/fleets
Authorization: Bearer {token}
```

### 创建车队

```http
POST /api/fleets
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "contact_person": "string",
  "phone": "string",
  "address": "string"
}
```

## 订单管理

### 获取订单列表

```http
GET /api/orders?platform_id=1&start_date=2025-01-01&end_date=2025-01-31
Authorization: Bearer {token}
```

### 导入订单数据

```http
POST /api/orders/import
Authorization: Bearer {token}
Content-Type: multipart/form-data

platform_id: 1
file: [Excel文件]
```

## 数据导出

### 导出数据

```http
POST /api/export/data
Authorization: Bearer {token}
Content-Type: application/json

{
  "table_name": "orders",
  "conditions": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "format": "excel"
}
```

## 对账中心

### 获取车队余额

```http
GET /api/reconciliation/balance?year=2025&month=1
Authorization: Bearer {token}
```

### 执行月度结算

```http
POST /api/reconciliation/monthly-settlement
Authorization: Bearer {token}
Content-Type: application/json

{
  "year": 2025,
  "month": 1
}
```

## 错误码说明

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 通用响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

## 分页响应格式

```json
{
  "code": 200,
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "per_page": 20,
    "pages": 5
  }
}
```
