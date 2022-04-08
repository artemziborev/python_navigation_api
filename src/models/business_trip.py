import mongoengine as me


class BusinessTrip(me.Document):
    name = me.StringField(required=True)
    destinations = me.ListField(required=True)
    business = me.BooleanField()


class PenguinTripsCount(me.Document):
    name = me.StringField(required=True)
    count = me.IntField(required=True)


class DestinationsCount(me.Document):
    name = me.StringField(required=True)
    count = me.IntField(required=True)
