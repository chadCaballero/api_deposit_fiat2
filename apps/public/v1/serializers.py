from apps import ma
# from marshmallow import Schema, fields

class CountrySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','name', 'status')