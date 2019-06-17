from apps import ma
from marshmallow import Schema, fields


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','username', 'email', 'password', 'dni','comment')

    # _links = ma.Hyperlinks({
    #     'self': ma.URLFor('user_detail', id='<id>'),
    #     'collection': ma.URLFor('users')
    # })


class UserSchema2(Schema):

    id = fields.Integer()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    dni = fields.Str()
    comment = fields.Str()