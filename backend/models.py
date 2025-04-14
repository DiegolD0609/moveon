from .app import db  # Se importa la instancia de la base de datos desde app.py

# Se definen los modelos de la base de datos
class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    first_lastname = db.Column(db.String(50), nullable=False)
    second_lastname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    # Relaciones
    motorbike_id = db.Column(db.Integer, db.ForeignKey('motorbikes.id'))
    motorbike = db.relationship('Motorbike', back_populates='customers')
    
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('Branch', back_populates='customers')

class Motorbike(db.Model):
    __tablename__ = 'motorbikes'
    
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    year = db.Column(db.String(30), nullable=False)
    
    # Se establece la relacion entre customers y branches
    customers = db.relationship('Customer', back_populates='motorbike')
    branches = db.relationship('Branch', back_populates='motorbike')

class Branch(db.Model):
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Se establece la relación con motorbikes y customers
    motorbike_id = db.Column(db.Integer, db.ForeignKey('motorbikes.id'))
    motorbike = db.relationship('Motorbike', back_populates='branches')
    customers = db.relationship('Customer', back_populates='branch')

def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "address": self.address,
        "latitude": self.latitude,
        "longitude": self.longitude,
        "motorbike_id": self.motorbike_id
    }    