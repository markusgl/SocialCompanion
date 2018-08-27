""" Schema for mapping other NLU-Schemas to fit to rasa """
from marshmallow import Schema, fields


class NLUResponse:
    def __init__(self, text=None, intent=None, entities=None):
        self.text = text
        self.intent = intent
        self.entities = entities


class IntentSchema(Schema):
    name = fields.Str()
    confidence = fields.Float()


class EntitiesSchema(Schema):
    start = fields.Int()
    end = fields.Int()
    value = fields.Str()
    entity = fields.Str()


class RasaNLUSchema(Schema):
    text = fields.Str()
    intent = fields.Nested(IntentSchema)
    entities = fields.List(fields.Nested(EntitiesSchema))
