from flask import request, jsonify, Blueprint
from Shop import cloudinary
from Shop.models import User, Data
import random
import base64
from .extension import db, bcrypt, mail
from flask_mail import Message
from flask_jwt_extended  import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, current_user



api_blue = Blueprint(
    'api',
    __name__
)

# Creating random One-Time-Password
OTP = random.randint(1000, 9999)


# # Creating the Homepage route
# @api_blue.route('/')
# @jwt_required()
# def Index():
#     all_data = []
#     if User.is_authenticated:
#         all_data = Data.query.filter_by(user_id=current_user.id).all()
#     else:
#         pass
#     return jsonify({
#         'data': all_data
#     })


# Creating the add-item route
@api_blue.route('/insert', methods=['POST'])
@jwt_required()
# @login_required
def insert():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    image_ = request.files.get('image', None)
    print(image_)
    
    current_user = get_jwt_identity()
    
    # Data validation
    if not name or not quantity:
        return jsonify({
            "message": "Please fill all the fields",
            "status": 400
        }), 400
    
    if image_:
        
        # image = base64.b64decode(image_)
        # try:
        #     upload_result = cloudinary.uploader.upload(image)
        #     image_url = upload_result.get('secure_url')
            
        new_item = Data(name=name, quantity=quantity, user_id=current_user, image_url=image_)
        # except Exception as e:
        #     return jsonify({
        #         "message": "Image upload failed with error: " + str(e),
        #         "status": 500
        #     }), 500
    else:
        new_item = Data(name=name, quantity=quantity, user_id=current_user)    

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": "Item Added Successfully",
        "status": 201
    })
    
    

# # Creating the update-item route
@api_blue.route('/update', methods=['POST'])
@jwt_required()
def update():
        item_id = request.json.get('id')
        item = Data.query.get(item_id)
        
        if not item:
            return jsonify({
                "message": "Item not found",
                "status": 400
            })

        item.name = request.json.get['name']
        # item.price = request.form['price']
        item.quantity = request.json.get['quantity']
        db.session.commit()

        return jsonify({
            "message": "Item Updated Successfully",
            "status": 200
        })
    
# Creating the delete-item  route
@api_blue.route('/delete/<int:id>/', methods=['GET', 'POST'])
@jwt_required()
def delete(id):
    item = Data.query.get(id)
    if not item:
        return jsonify({
            "message": "Item not found",
            "status": 400
        })

    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "message": "Item Deleted Successfully",
        "status": 200
    })




# Creating the register-user route
@api_blue.route('/register', methods=['POST'])
def register():
# Preventing the user from logging in again if already logged in
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({
            "message": "Username already taken",
            "status": 400
        })
    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Email already taken",
            "status": 400
        })
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User registered successfully",
        "status": 201
    })


# # # Creating the OTP email
# # def send_otp(email):
# #     msg = Message('Verification Token', sender='Anonymous@gmail.com', recipients=[email])
# #     msg.body = f'Your verification token is: {OTP}'
# #     mail.send(msg)



# # Creating the login route
@api_blue.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({
            "message": "Please enter all fields",
            "status": 400
        })
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "message": "Username not found",
            "status": 400
        })
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Incorrect password"
        }), 400
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({
        "message": "Login successful",
        "status": 200,
        "access_token" : access_token,
        "refresh_token" : refresh_token
    })
    
# dashboard
@api_blue.route('/view', methods=['GET'])
@jwt_required()
def dashboard():
    return jsonify({
        "message": "Dashboard",
        "status": 200
    })


# # # # Creating the logout route
# @api_blue.route('/logout', methods=['POST'])
# @jwt_required
# def logout():
#     return jsonify({
#         "message": "Logout successful",
#         "status": 200
#     })


# # # # # Creating the user-items route
@api_blue.route('/get_items',  methods=['GET'])
@jwt_required()
def get_items():
    user_id = get_jwt_identity()
    all_data = Data.query.filter_by(user_id=user_id).all()
    return jsonify({
        "message": "Items retrieved successfully",
        "status": 200,
        "items": [data.as_dict() for data in all_data]
    })
    
    
    


# Creating the admin route for viewing the registered users
@api_blue.route('/admin_users', methods=['GET'])
@jwt_required()
def admin_users():
    if not User.query.get(get_jwt_identity()).is_admin:
        return jsonify({
            "message": "You are not authorized to perform this action!",
            "status": 400
        })
    else:
        all_users = [
            
        ]
        users = User.query.all()
        for user in users:
            all_users.append({
                "username": user.username,
                "email": user.email,
                "id":user.id
            })
        return jsonify({
            "message": "Users retrieved successfully",
            "status": 200,
            "users": all_users
        })

# # # Creating the admin route for viewing users
@api_blue.route('/admin_view', methods=['GET'])
@jwt_required()
def admin_view():
    if not User.query.get(get_jwt_identity()).is_admin:
        return jsonify({
            "message": "You are not authorized to perform this action!",
            "status": 400
        })
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify({
        "message": "Users retrieved successfully",
        "status": 200,
        "users": users_list
    })

# # # Creating the admin route for deleting users
@api_blue.route('/admin/delete_user/<int:user_id>/', methods=['DELETE'])
@jwt_required()
def admin_delete_user(user_id):
    if not User.query.get(get_jwt_identity()).is_admin:
        return jsonify({
            "message": "You are not authorized to perform this action!",
            "status": 400
        })
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "message": "User not found",
            "status": 404
        })
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "message": "User deleted successfully",
        "status": 200
    })


# # # Creating the admin route for viewing user-items
@api_blue.route('/admin/view_user_items/<int:user_id>/', methods=['GET'])
@jwt_required()
def view_user_items(user_id):
    if not User.query.get(get_jwt_identity()).is_admin:
        return jsonify({
            "message": "You are not authorized to perform this action!",
            "status": 400
        })

    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "message": "User not found",
            "status": 404
        })
        
    items = Data.query.filter_by(user_id=user.id).all()
    return jsonify({
        "message": "Items retrieved successfully",
        "status": 200,
        "items": items
    })



# Creating the verify OTP for registering users
@api_blue.route('/verify_otp/<string:email>/', methods=['GET', 'POST'])
@jwt_required()
def verify_otp(email):
    if request.method == 'POST':
        otp = request.form.get('otp')
        if otp is None:
            return jsonify({
                "message": "OTP not provided",
                "status": 400
            }), 400

        user = User.query.filter_by(email=email).first()

        try:
            if int(otp) != OTP:
                return jsonify({
                    "message": "Incorrect OTP",
                    "status": 400
                }), 400
        except ValueError:
            return jsonify({
                "message": "Invalid OTP format",
                "status": 400
            }), 400

        user.is_verified = True
        db.session.commit()
        return jsonify({
            "message": "OTP verified successfully",
            "status": 200
        }), 200
    else:
        return jsonify({
            "message": "Only POST method is allowed",
            "status": 405
        }), 405
