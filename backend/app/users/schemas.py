from marshmallow import Schema, fields, pre_load

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)

    @pre_load
    def normalize_input(self, data, **kwargs):
        data["email"] = data.get("email", "").lower()
        data["username"] = data.get("username", "").lower()
        return data

class UpdateUserSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)

    @pre_load
    def normalize_input(self, data, **kwargs):
        data["email"] = data.get("email", "").lower()
        data["username"] = data.get("username", "").lower()
        return data

user_schema = UserSchema()
users_schema = UserSchema(many=True)
updateUser_schema = UpdateUserSchema()
