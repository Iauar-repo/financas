from marshmallow import Schema, fields, pre_load, validate


class ListUserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


class CreateUserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=8)
    )
    recaptcha_token = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=1)
    )

    @pre_load
    def normalize_input(self, data, **kwargs):
        data["email"] = data.get("email").lower()
        return data


class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))


class UpdateUserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))


list_user_schema = ListUserSchema()
list_users_schema = ListUserSchema(many=True)
update_user_schema = UpdateUserSchema()
create_user_schema = CreateUserSchema()
