from functools import wraps
from flask import request, jsonify
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from werkzeug.security import generate_password_hash, check_password_hash
import connexion
import pytz
from datetime import timedelta
import datetime

flask_app = connexion.FlaskApp(__name__, specification_dir="./")
app = flask_app.app
flask_app.add_api("Swagger.yml")

app.config["JWT_SECRET_KEY"] = "08a44d92-588c-4cd5-988b-c665ecdd4f40"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)

gmt_plus_8 = pytz.timezone("Asia/Singapore")
current_time_gmt_plus_8 = datetime.datetime.now(gmt_plus_8)

client = MongoClient("mongodb+srv://20220024573:T7CmWQ47ed9s8kpv@recipecluster.81ir5.mongodb.net/")
db = client["ActiveDirectory_API"]
student_collection = db["Students"]
users_collection = db["Users"]
role_collection = db["Roles"]

## FUNCTIONS
def session_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with app.app_context():
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                return jsonify({"error": "Missing token in session"}), 401
            try:
                token_data = decode_token(token.split(" ")[1])
                request.user_role = token_data.get("role")
                request.user_id = token_data.get("sub")
            except Exception as e:
                return jsonify({"error": "Token validation failed", "message": str(e)}), 401
            return fn(*args, **kwargs)
    return wrapper

def checkKey(userID):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return {"msg": "Missing token in session"}, 401

    token_data = decode_token(token.split(" ")[1])
    role = token_data.get("role")
    user = token_data.get("sub")
    
    if role == 'admin':
        return 1

    if user == userID and role != "regular":
        return 1

    return 0

def getRoles():
    role_available = role_collection.find({}, {"_id": 0, "name": 1})
    roles = [role.get("name", "") for role in role_available]
    return roles

def getStudents(students):
    response = []
    for student in students:
        response.append(
                {
                    'studentid': student['studentid'],
                    'fullname': student['fullname'],
                    'course': student('course'),
                    'yearlevel': student('yearlevel'),
                    'email': student('email'),
                    'contactnumber': student('contactnumber'),
                    'address': student('address')
                }
            )
    return response
    
def _updateRecipe(userID, studentid, method):
    role = checkKey(userID)
    if role == 0:
        return jsonify({'message': "Forbidden to update recipe information."}), 403
    
    student_data = student_collection.find_one({'studentid': studentid})
    
    if student_data is None:
        return jsonify ({'error': "No recipe found."}), 404
    
    data = request.get_json()

    #Student data
    studentid = data.get('studentid', student_data['studentid'])
    fullname = data.get('fullname',student_data['fullname'])
    course = data.get('course',student_data['course'])
    yearlevel = data.get('yearlevel',student_data['yearlevel'])
    email = data.get('email',student_data['email'])
    contactnumber = data.get('contactnumber',student_data['contactnumber'])
    address = data.get('address',student_data['address'])
    
    
    StudentInfo_update = {
        'studentid': studentid,
        'fullname': fullname,
        'course': course,
        'yearlevel': yearlevel,
        'email': email,
        'contactnumber': contactnumber,
        'address': address,
    }
    
    student_collection.update_one({'studentid':studentid }, {'$set': StudentInfo_update}) 
    
    return jsonify({'message': 'Student information updated successfully.'}), 200


## (POST) USER CREATE
@app.route('/users/create', methods=['POST'])
def createUser():
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format.'}), 400
    
    user_data = request.get_json()
    username = user_data.get('username')
    password = user_data.get('password')
    name = user_data.get('name')
    email = user_data.get('email')
    role = user_data.get('role')
    
    roles = getRoles()
    
    if not username or not password or not name or not email or not role:
        return jsonify({'error': 'All fields (username, password, name, email, role) are required'}), 400
    
    if users_collection.find_one({'userID': username}):
        return jsonify({'error': 'Username already exists.'}), 409
    
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'Email already registered.'}), 409
    
    if not role in roles:
        return jsonify({'error': 'roles not in the options.'}), 409
    
    hashpass = generate_password_hash(password)
    
    new_user = {
        'userID': username,
        'password': hashpass,
        'name': name,
        'email': email,
        'role': role
    }
    users_collection.insert_one(new_user)
    
    return jsonify({'message': 'User created successfully.'}), 201
    

## (POST) USER LOG IN
@app.route('/users/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format.'}), 400
    
    user_data = request.get_json()
    username = user_data.get('username')
    password = user_data.get('password')
        
    if not username or not password:
        return jsonify({'error': "Both 'username' and 'password' fields are required."}), 401
    
    user = users_collection.find_one({'userID': username})
    
    if not user:
        return jsonify({'error': "Invalid username."}), 401
    
    if not check_password_hash(user['password'], password): 
        return jsonify({'error': "Invalid  password."}), 401
    
    apiKey = create_access_token(
        identity=username, 
        additional_claims={
            'email': user['email'],
            'role': user['role'],
            'name': user.get('name', 'Unknown'),
            'datetime_created': current_time_gmt_plus_8.strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
    return jsonify({'message': 'Login successful.', 'apiKey': apiKey}), 201


## (DELETE) USER DELETE
@app.route('/users/<userID>', methods=['DELETE'])
@session_jwt_required
def deleteUser(userID):
    role = checkKey(userID)
    if role == 0:
        if userID != request.user_id:
            return jsonify({'message': "Forbidden to delete account."}), 403
        
    if request.is_json:
        user_data = request.get_json()
        password = user_data.get('password')
        
    if  not password:
        return jsonify({'error': "Password is required for confirmation."}), 400
    
    user = users_collection.find_one({'userID': userID})
    
    if not user:
        return jsonify({'error': "User not found."}), 404
    
    if not check_password_hash(user['password'], password):  
        return jsonify({'error': "Invalid  password."}), 403
    
    users_collection.delete_one({'userID': userID})
    return jsonify({'message': "User deletion successful."}), 200


## (GET) ALL RECIPE (OKAY)
@app.route('/students', methods=['GET'])
@session_jwt_required
def getAll():

    studentid = request.args.get('studentid')
    fullname = request.args.get('fullname')

    query = {}

    if studentid: 
        query['studentid'] = {'$regex': f'^{studentid}$', '$options': 'i'}
    if fullname:
        query['fullname'] = {'$regex': f'^{fullname}$', '$options': 'i'}

    student = student_collection.find(query, {'_id': 0})
    response = getStudents(student)
    return jsonify(response), 200


## (GET) SPECIFIC RECIPE DATA (OKAY)
@app.route('/students/<int:studentid>', methods=['GET'])
@session_jwt_required
def getSpecificStudent(studentid):
        student_count = student_collection.count_documents({'studentid': studentid})
        
        if student_count == 0:
            return jsonify({"error": f"Student '{studentid}' not found"}), 404
        
        recipe = student_collection.find({'studentid': studentid}, {'_id': 0})
        response = getStudents(recipe)
        return jsonify(response), 200


## (POST) USER CREATE A RECIPE (Student OKAY, userID NOT)
@session_jwt_required
def createStudentInfo(userID):
    
    role = checkKey(userID)
    if role == 0:
        return jsonify({'error': "Forbidden access."}), 403     
    data = request.get_json()
    
    user = users_collection.find_one({'userID': userID})
    if user is None:
        return jsonify({'error': "User not found."}), 404
    
    #Student data
    studentid = data.get('studentid', '')
    fullname = data.get('fullname','')
    course = data.get('course','')
    yearlevel = data.get('yearlevel','')
    email = data.get('email','')
    contactnumber = data.get('contactnumber','')
    address = data.get('address','')
    
    if not studentid or not fullname or not type or not course or not yearlevel or not email or not contactnumber or not address:
        return jsonify({'error': "All fields are required."}), 400
    

    new_studentInfo = {
        'studentid': studentid,
        'fullname': fullname,
        'course': course,
        'yearlevel': yearlevel,
        'email': email,
        'contactnumber': contactnumber,
        'address': address,
    }

    
    student_collection.insert_one(new_studentInfo)
    
    return jsonify({'message': 'StudentInfo created successfully.'}), 201



## (PUT) UPDATE A SPECIFIC RECIPE (OKAY)
@session_jwt_required
def updateSpecificStudentByUser(userID, studentid):
    return _updateRecipe(userID, studentid, request.method)


## (PATCH) UPDATE A SPECIFIC RECIPE (OKAY)
@session_jwt_required
def partialUpdateSpecificStudentByUser(userID, studentid):
    return _updateRecipe(userID, studentid, request.method)


if __name__ == "__main__":
    with app.app_context():
        flask_app.run(port=4000)