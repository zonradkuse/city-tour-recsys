# src models/ShopModel.py

from marshmallow import fields, Schema
from . import db

class ShopModel(db.Model):
    """
    ShopModel
    """

    #table name
    __tablename__='shops'

    id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.String(255),nullable=True)
    node_id=db.Column(db.Integer,db.ForeignKey('nodes.id'),nullable=False)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.type = data.get('type')
        self.node_id = data.get('node_id')

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
    def get_all_shops():
        return ShopModel.query.all()

    @staticmethod
    def get_one_shop(id):
        return ShopModel.query.get(id)

class ShopSchema(Schema):
    """
    Shop Schema
    """
    id = fields.Int(dump_only=True)
    type=fields.Str(required=True)
    node_id = fields.Int(required=True)
