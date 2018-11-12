# src/models/NodeModel.py

from marshmallow import fields, Schema
from . import db
from .AmenityModel import AmenitySchema
from .ShopModel import ShopSchema
from .TourismModel import TourismSchema

class NodeModel(db.Model):
    """
    NodeModel
    """

    #table name
    __tablename__='nodes'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    image_link=db.Column(db.Text,nullable=True)
    website=db.Column(db.Text,nullable=True)
    lon=db.Column(db.Float,nullable=False)
    lat=db.Column(db.Float,nullable=False)
    description=db.Column(db.Text,nullable=True)
    phone=db.Column(db.String(255),nullable=True)
    email=db.Column(db.String(500),nullable=True)
    amenities=db.relationship('AmenityModel',backref='users',lazy=True)
    tourism=db.relationship('TourismModel',backref='users',lazy=True)
    shops=db.relationship('ShopswModel',backref='users',lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.image_link=data.get('image_link')
        self.website=data.get('website')
        self.lon=data.get('lon')
        self.lat=data.get('lat')
        self.description=data.get('description')
        self.phone=data.get('phone')
        self.email=data.get('email')

    def save(self):
        db.session.add(self)
        db.session.commit()


    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_nodes():
        return NodeModel.query.all()

    @staticmethod
    def get_one_nodes(id):
        return NodeModel.query.get(id)

class NodeSchema(Schema):
    """
    Node Schema
    """
    id = fields.Int(dump_only=True)
    name=fields.Str(required=True)
    image_link = fields.Str(required=True)
    website = fields.Str(required=True)
    lon= fields.Float(required=True)
    lat = fields.Float(required=True)
    description = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Str(required=True)
    amenities = fields.Nested(AmenitySchema, many=True)
    tourism = fields.Nested(TourismSchema, many=True)
    shops = fields.Nested(ShopSchema, many=True)
