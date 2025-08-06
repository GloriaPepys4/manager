from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import jwt
import uuid
from functools import wraps
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')

# 初始化CORS
CORS(app)

# Supabase配置
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://your-project.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', 'your-anon-key')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', 'your-service-key')

# 创建Supabase客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# JWT工具函数
def create_access_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    # 明确指定算法参数以兼容新版本PyJWT
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    try:
        # 明确指定算法列表以兼容新版本PyJWT
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# JWT装饰器
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'code': 401, 'message': '无效的token格式'}), 401
        
        if not token:
            return jsonify({'code': 401, 'message': '缺少认证token'}), 401
        
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'code': 401, 'message': 'token无效或已过期'}), 401
        
        # 将用户ID添加到请求上下文
        request.current_user_id = user_id
        return f(*args, **kwargs)
    
    return decorated_function

# 认证路由
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
        
        if not username or not email or not password:
            return jsonify({
                'code': 400,
                'message': '用户名、邮箱和密码不能为空'
            }), 400
        
        # 检查用户名是否已存在
        existing_user = supabase.table('users').select('id').eq('username', username).execute()
        if existing_user.data:
            return jsonify({
                'code': 400,
                'message': '用户名已存在'
            }), 400
        
        # 检查邮箱是否已存在
        existing_email = supabase.table('users').select('id').eq('email', email).execute()
        if existing_email.data:
            return jsonify({
                'code': 400,
                'message': '邮箱已存在'
            }), 400
        
        # 创建新用户
        user_data = {
            'id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password, method='scrypt'),
            'role': role
        }
        
        result = supabase.table('users').insert(user_data).execute()
        
        if result.data:
            user = result.data[0]
            access_token = create_access_token(user['id'])
            return jsonify({
                'code': 200,
                'message': '注册成功',
                'data': {
                    'token': access_token,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role'],
                        'created_at': user['created_at']
                    }
                }
            })
        else:
            return jsonify({
                'code': 500,
                'message': '注册失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'code': 400,
                'message': '用户名和密码不能为空'
            }), 400
        
        # 从Supabase查询用户
        result = supabase.table('users').select('*').eq('username', username).execute()
        
        if not result.data:
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
        
        user = result.data[0]
        
        # 验证密码
        if check_password_hash(user['password_hash'], password):
            access_token = create_access_token(user['id'])
            return jsonify({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'token': access_token,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role'],
                        'created_at': user['created_at']
                    }
                }
            })
        else:
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required
def get_current_user():
    try:
        user_id = request.current_user_id
        
        # 从Supabase查询用户信息
        result = supabase.table('users').select('id, username, email, role, created_at').eq('id', user_id).execute()
        
        if result.data:
            return jsonify({
                'code': 200,
                'data': result.data[0]
            })
        else:
            return jsonify({
                'code': 404,
                'message': '用户不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

# 车辆管理路由
@app.route('/api/vehicles', methods=['GET'])
@jwt_required
def get_vehicles():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        keyword = request.args.get('keyword', '')
        
        # 计算偏移量
        offset = (page - 1) * per_page
        
        # 构建查询
        query = supabase.table('vehicles').select('*, fleets(name)')
        
        if keyword:
            # Supabase使用ilike进行模糊搜索
            query = query.or_(f'license_plate.ilike.%{keyword}%,vehicle_type.ilike.%{keyword}%,driver_name.ilike.%{keyword}%')
        
        # 获取总数
        count_result = supabase.table('vehicles').select('id', count='exact')
        if keyword:
            count_result = count_result.or_(f'license_plate.ilike.%{keyword}%,vehicle_type.ilike.%{keyword}%,driver_name.ilike.%{keyword}%')
        count_data = count_result.execute()
        total = count_data.count
        
        # 获取分页数据
        result = query.range(offset, offset + per_page - 1).execute()
        
        # 处理数据格式
        vehicles = []
        for vehicle in result.data:
            vehicle_data = {
                'id': vehicle['id'],
                'license_plate': vehicle['license_plate'],
                'vehicle_type': vehicle['vehicle_type'],
                'fleet_id': vehicle['fleet_id'],
                'fleet_name': vehicle['fleets']['name'] if vehicle['fleets'] else None,
                'driver_name': vehicle['driver_name'],
                'driver_phone': vehicle['driver_phone'],
                'status': vehicle['status'],
                'remark': vehicle['remark'],
                'created_at': vehicle['created_at']
            }
            vehicles.append(vehicle_data)
        
        return jsonify({
            'code': 200,
            'data': {
                'items': vehicles,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/vehicles', methods=['POST'])
@jwt_required
def create_vehicle():
    try:
        data = request.get_json()
        
        # 检查车牌号是否已存在
        existing = supabase.table('vehicles').select('id').eq('license_plate', data['license_plate']).execute()
        if existing.data:
            return jsonify({
                'code': 400,
                'message': '车牌号已存在'
            }), 400
        
        # 创建车辆记录
        vehicle_data = {
            'license_plate': data['license_plate'],
            'vehicle_type': data['vehicle_type'],
            'fleet_id': data['fleet_id'],
            'driver_name': data.get('driver_name'),
            'driver_phone': data.get('driver_phone'),
            'status': data.get('status', 'active'),
            'remark': data.get('remark')
        }
        
        result = supabase.table('vehicles').insert(vehicle_data).execute()
        
        return jsonify({
            'code': 200,
            'message': '车辆创建成功',
            'data': result.data[0]
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/vehicles/<vehicle_id>', methods=['PUT'])
@jwt_required
def update_vehicle(vehicle_id):
    try:
        data = request.get_json()
        
        # 检查车辆是否存在
        existing = supabase.table('vehicles').select('id').eq('id', vehicle_id).execute()
        if not existing.data:
            return jsonify({
                'code': 404,
                'message': '车辆不存在'
            }), 404
        
        # 如果更新车牌号，检查是否重复
        if 'license_plate' in data:
            duplicate = supabase.table('vehicles').select('id').eq('license_plate', data['license_plate']).neq('id', vehicle_id).execute()
            if duplicate.data:
                return jsonify({
                    'code': 400,
                    'message': '车牌号已存在'
                }), 400
        
        # 更新车辆信息
        update_data = {}
        for key in ['license_plate', 'vehicle_type', 'fleet_id', 'driver_name', 'driver_phone', 'status', 'remark']:
            if key in data:
                update_data[key] = data[key]
        
        result = supabase.table('vehicles').update(update_data).eq('id', vehicle_id).execute()
        
        return jsonify({
            'code': 200,
            'message': '车辆更新成功',
            'data': result.data[0]
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/vehicles/<vehicle_id>', methods=['DELETE'])
@jwt_required
def delete_vehicle(vehicle_id):
    try:
        # 检查车辆是否存在
        existing = supabase.table('vehicles').select('id').eq('id', vehicle_id).execute()
        if not existing.data:
            return jsonify({
                'code': 404,
                'message': '车辆不存在'
            }), 404
        
        # 删除车辆
        supabase.table('vehicles').delete().eq('id', vehicle_id).execute()
        
        return jsonify({
            'code': 200,
            'message': '车辆删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

# 车队管理路由
@app.route('/api/fleets', methods=['GET'])
@jwt_required
def get_fleets():
    try:
        result = supabase.table('fleets').select('*').execute()
        return jsonify({
            'code': 200,
            'data': result.data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

# 根路由
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'code': 200,
        'message': '数据整合平台API',
        'version': '1.0.0'
    })

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'code': 200,
        'message': 'API服务正常运行',
        'timestamp': datetime.utcnow().isoformat()
    })

# Vercel函数入口点
def handler(request):
    return app(request.environ, lambda *args: None)

# 本地开发时的入口点
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)