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

RESPONSE
``json 
{
    "message": "User registered successfully"
}

POST (Login) /api/login


REQUEST
```json
{
  "email": "user@example.com", 
  "password": "string"
}
```
RESPONSE
```json
  {
    "key": "eyJhbGciOiJIUzIEyM...................",
  }
```

To login with your key,

```sh
Token <key>
```
`
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


POST (Verifying OTP) api/verify_otp/<string:email>/
@jwt_required
RESPONSE
json

{
    "message": "OTP verified successfully"
}