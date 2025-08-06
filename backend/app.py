from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 车队模型
class Fleet(db.Model):
    __tablename__ = 'fleets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    contact_person = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 车辆模型
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleets.id'), nullable=False)
    driver_name = db.Column(db.String(50))
    driver_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='normal')
    remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    fleet = db.relationship('Fleet', backref=db.backref('vehicles', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'plate_number': self.plate_number,
            'vehicle_type': self.vehicle_type,
            'fleet_id': self.fleet_id,
            'fleet_name': self.fleet.name if self.fleet else None,
            'driver_name': self.driver_name,
            'driver_phone': self.driver_phone,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 认证路由
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
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'token': access_token,
                    'user': user.to_dict()
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
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user:
            return jsonify({
                'code': 200,
                'data': user.to_dict()
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
@jwt_required()
def get_vehicles():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        keyword = request.args.get('keyword', '')
        
        query = Vehicle.query
        
        if keyword:
            query = query.filter(
                db.or_(
                    Vehicle.plate_number.contains(keyword),
                    Vehicle.vehicle_type.contains(keyword),
                    Vehicle.driver_name.contains(keyword)
                )
            )
        
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        vehicles = [vehicle.to_dict() for vehicle in pagination.items]
        
        return jsonify({
            'code': 200,
            'data': {
                'items': vehicles,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/vehicles', methods=['POST'])
@jwt_required()
def create_vehicle():
    try:
        data = request.get_json()
        
        # 检查车牌号是否已存在
        existing_vehicle = Vehicle.query.filter_by(plate_number=data['plate_number']).first()
        if existing_vehicle:
            return jsonify({
                'code': 400,
                'message': '车牌号已存在'
            }), 400
        
        vehicle = Vehicle(
            plate_number=data['plate_number'],
            vehicle_type=data['vehicle_type'],
            fleet_id=data['fleet_id'],
            driver_name=data.get('driver_name'),
            driver_phone=data.get('driver_phone'),
            status=data.get('status', 'normal'),
            remark=data.get('remark')
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '车辆创建成功',
            'data': vehicle.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

# 车队管理路由
@app.route('/api/fleets', methods=['GET'])
@jwt_required()
def get_fleets():
    try:
        fleets = Fleet.query.all()
        return jsonify({
            'code': 200,
            'data': [fleet.to_dict() for fleet in fleets]
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500

# 初始化数据库
def create_tables():
    db.create_all()
    
    # 创建默认管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 创建默认车队
        fleets = [
            Fleet(name='快运车队', description='专业快运服务', contact_person='张经理', contact_phone='13800138001'),
            Fleet(name='城际运输', description='城际货运服务', contact_person='李经理', contact_phone='13800138002'),
            Fleet(name='同城配送', description='同城配送服务', contact_person='王经理', contact_phone='13800138003')
        ]
        
        for fleet in fleets:
            db.session.add(fleet)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)