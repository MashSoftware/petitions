from application import db
from geoalchemy2 import Geometry


class Constituency(db.Model):
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    area_code = db.Column(db.String(3))
    description = db.Column(db.String(50))
    file_name = db.Column(db.String(50))
    number = db.Column(db.Float(precision=8))
    number0 = db.Column(db.Float(precision=8))
    polygon_id = db.Column(db.Float(precision=8))
    unit_id = db.Column(db.Float(precision=8))
    code = db.Column(db.String(9))
    hectares = db.Column(db.Float(precision=8))
    area = db.Column(db.Float(precision=8))
    type_code = db.Column(db.String(2))
    descript0 = db.Column(db.String(25))
    type_cod0 = db.Column(db.String(3))
    descript1 = db.Column(db.String(36))
    geom = db.Column(Geometry('MULTIPOLYGON'))

    def __init__(self, arg):
        super(Constituency, self).__init__()
        self.arg = arg
