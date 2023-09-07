# Shopping-Cart-API

### Endpoints

POST (Register) /api/register

To get registered as an admin, make sure the is_admin variable is set to True else you'll be regiatered as a user

REQUEST
```json
{
  "firstname": "string",
  "password1": "string",
  "email": "string@string.com"
}
```

RESPONSE
```json 
{
    "message": "User registered successfully",
    "Info" : "Please verify your account with the OTP sent to your email",
    "status": 201
}
```
POST (Verify Otp) /api/verify_otp/<email>


REQUEST
```json 
{
    "otp": "7854"
}
```
RESPONSE
```json
{
    "message": "OTP verified successfully",
    "status": 200
}
```

POST (Login) /api/login


REQUEST
```json
{
    "username": "Admin",
    "email" : "admin_email",
    "password": "pass"
}
```
RESPONSE
```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..............................",
    "message": "Login successful",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9........................",
    "status": 200
}
```

To login with your access_token in the Authorization holder in the bearer token section,

```sh
<access_token>
```

<!-- To add an item to cart -->
POST api/insert 
@jwt_required()
@login_required

REQUEST
```json
{
    "name": "string",
    "quantity": "int",
    "image": "url or default",
}
```
RESPONSE
```json
  {
  "message": "item added successfully"
}
```

POST (Update) /api/update/<int:id>

REQUEST
```json
{
  "name": "string",
  "quantity": "int"
}
```
RESPONSE
```json
  {
  "message": "Items updated successfully"
}
```

POST (Delete item)  /api/delete/<int:id>/
@login_required

RESPONSE
```json
{
  "message": "Item deleted successfully"
}
```

GET (Showing added items) /api/get_items 
@login_required

RESPONSE
```json
  {
    "message" : "Items retreived successfully"
  }


GET (Showing users) api/admin_users
@jwt_required

RESPONSE
json
{
    "message": "Users retreived successfully"
}


DELETE (Deleting users)   api/admin/delete_user/<int:user_id>
@jwt_required
RESPONSE
json
{
    "message": "User deleted successfully"
}


GET (Displaying user added items)  api/admin/view_user_items/<int:user_id>
@jwt_required
RESPONSE
json
{
    "message" : "Items retreived successfully"
}


// POST (Verifying OTP) api/verify_otp/<string:email>/
// @jwt_required
// RESPONSE
// json

// {
//     "message": "OTP verified successfully"
// }