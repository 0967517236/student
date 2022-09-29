from marshmallow import Schema, fields


class StudentCreateSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    mediumScore = fields.Float(required=True)
    result = fields.Boolean(required=True)
    classRoom = fields.Str(required=True)
    phone = fields.Float(required=True)
    address = fields.Str(required=True)
    email = fields.Email(required=True)


class StudentUpdateSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    mediumScore = fields.Float(required=True)
    result = fields.Boolean(required=True)
    classRoom = fields.Str(required=True)
    phone = fields.Float(required=True)
    address = fields.Str(required=True)
    email = fields.Email(required=True)
