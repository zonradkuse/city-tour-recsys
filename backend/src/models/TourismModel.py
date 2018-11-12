# src models/TourismModel.py

from marshmallow import fields, Schema
from . import db

class TourismModel(db.Model):
    """
    TourismModel
    """

    #table name
    __tablename__='tourism'

    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.Text,nullable=True)
    type=db.Column(db.String(255),nullable=True)
    node_id=db.Column(db.Integer,db.ForeignKey('nodes.id'),nullable=False)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.description = data.get('description')
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
    def get_all_tourism():
        return TourismModel.query.all()

    @staticmethod
    def get_one_tourism(id):
        return TourismModel.query.get(id)

class TourismSchema(Schema):
    """
    Tourism Schema
    """
    id = fields.Int(dump_only=True)
    description=fields.Str(required=True)
    type=fields.Str(required=True)
    node_id = fields.Int(required=True)
