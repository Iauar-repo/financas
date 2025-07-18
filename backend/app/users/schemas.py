from marshmallow import Schema, fields, pre_load, validate

class ListUserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    username = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

class CreateUserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
    recaptcha_token = fields.Str(required=True, load_only=True, validate=validate.Length(min=1))

    @pre_load
    def normalize_input(self, data, **kwargs):
        data["email"] = data.get("email").lower()
        data["username"] = data.get("username").lower()
        return data

class UpdateUserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    username = fields.Str(validate=validate.Length(min=1))
    email = fields.Email(validate=validate.Length(min=1))
    password = fields.Str(load_only=True, validate=validate.Length(min=8))

    @pre_load
    def normalize_input(self, data, **kwargs):
        data["email"] = data.get("email").lower()
        data["username"] = data.get("username").lower()
        return data

listUser_schema = ListUserSchema()
listUsers_schema = ListUserSchema(many=True)
updateUser_schema = UpdateUserSchema()
createUser_schema = CreateUserSchema()
