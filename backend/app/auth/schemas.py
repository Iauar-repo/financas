from marshmallow import Schema, fields, pre_load, validate


class LoginSchema(Schema):
    email = fields.Email(required=True, load_only=True, validate=validate.Length(min=1))
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=8)
    )


class CreateUserSocialSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    verified_email = fields.Bool()
    family_name = fields.Str()
    picture = fields.Str()
    given_name = fields.Str()

    @pre_load
    def normalize_input(self, data, **kwargs):
        data["email"] = data.get("email").lower()
        return data


login_schema = LoginSchema()
create_user_social_schema = CreateUserSocialSchema()
