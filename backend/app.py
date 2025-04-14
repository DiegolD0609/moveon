from flask import Flask, request, jsonify
from .models import db, Customer, Motorbike, Branch
from dotenv import load_dotenv
import os
from math import radians, sin, cos, sqrt, atan2
import requests
from time import sleep
from .extensions import db, cors

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        "postgresql://diego_lugo:6QzgDLILYzkJSva3FYQMBrUbp0ikIQeG@" \
        "dpg-cvu9efa4d50c73ara9i0-a.oregon-postgres.render.com:5432/moveondb"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'sslmode': 'require'
        }
    }
    
    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)
    
    with app.app_context():
        # Import models here to avoid circular imports
        from . import models
        db.create_all()
    
    return app

app = create_app()

# Constantes
EARTH_RADIUS_KM = 6371.0
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Configuración de la base de datos
def geocode_structured_address(address_components):
    """Handle structured address components for better accuracy"""
    params = {
        'street': f"{address_components.get('number', '')} {address_components.get('street', '')}".strip(),
        'city': address_components.get('city', ''),
        'state': address_components.get('state', ''),
        'country': address_components.get('country', ''),
        'postalcode': address_components.get('zipcode', ''),
        'format': 'json',
        'limit': 1
    }
    
    # Remover componentes vacíos
    params = {k: v for k, v in params.items() if v}
    
    for attempt in range(3):
        try:
            response = requests.get(
                NOMINATIM_URL,
                params=params,
                headers={'User-Agent': 'MotorbikeFinder/1.0'},
                timeout=5
            )
            
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                return {
                    'latitude': float(data['lat']),
                    'longitude': float(data['lon']),
                    'formatted_address': data['display_name']
                }
            sleep(1)  # Respetar los límites de la API
        except Exception as e:
            app.logger.warning(f"Geocoding attempt {attempt+1} failed: {str(e)}")
            sleep(2)
    
    app.logger.error(f"Geocoding failed for address components: {address_components}")
    return None
# Calcular la distancia entre dos puntos geográficos usando la fórmula de Haversine
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return EARTH_RADIUS_KM * c

# Geocodificar una dirección simple
@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Pre cargar datos de prueba
        # Se establecen las dos tablas de la base de datos: Customer y Motorbike
        if not Motorbike.query.first():
            bike1 = Motorbike(model='R6', brand='Yamaha', color='Blue', year='2020')
            bike2 = Motorbike(model='DUKE 390', brand='KTM', color='Orange' , year='2023')
            db.session.add_all([bike1, bike2])
            db.session.commit()
            print("Preloaded motorbike data!")
# Cargar una sucursal con información de geolocalización
@app.route('/api/branches', methods=['POST'])
def create_branch():

    data = request.get_json()
    required_fields = ['name', 'address', 'motorbike_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        motorbike = Motorbike.query.get(data['motorbike_id'])
        if not motorbike:
            return jsonify({"error": "Invalid motorbike_id"}), 400

        geo_data = geocode_address(data['address'])
        if not geo_data:
            return jsonify({"error": "Could not geocode address"}), 400

        branch = Branch(
            name=data['name'],
            address=geo_data['formatted_address'],
            latitude=geo_data['latitude'],
            longitude=geo_data['longitude'],
            motorbike_id=data['motorbike_id']
        )
        db.session.add(branch)
        db.session.commit()
        return jsonify({
            "id": branch.id,
            "name": branch.name,
            "address": branch.address,
            "coordinates": {
                "latitude": branch.latitude,
                "longitude": branch.longitude
            },
            "motorbike_id": branch.motorbike_id
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating branch: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Encontrar la sucursal más cercana
@app.route('/api/branches/nearest', methods=['POST'])
def get_nearest_branch():
    address_data = request.json
    
    # Validacion usando colonia, ciudad y pais
    required_fields = ['neighborhood', 'city', 'country']
    if not all(field in address_data for field in required_fields):
        return jsonify({
            "error": "Missing required fields",
            "required": required_fields,
            "received": list(address_data.keys())
        }), 400

    try:
        # Geocodificar la dirección estructurada
        # Se utiliza la función geocode_structured_address para obtener la latitud y longitud
        geo_data = geocode_structured_address({
            'street': address_data.get('street', ''),
            'number': address_data.get('number', ''),
            'neighborhood': address_data['neighborhood'],
            'city': address_data['city'],
            'state': address_data.get('state', ''),
            'country': address_data['country'],
            'zipcode': address_data.get('zipcode', '')
        })
        
        if not geo_data:
            return jsonify({"error": "Could not geocode address"}), 400

        ## Filtrar sucursales por motorbike_id cuando se proporciona
        query = Branch.query
        if 'motorbike_id' in address_data:
            query = query.filter_by(motorbike_id=address_data['motorbike_id'])
            
        branches = query.all()
        if not branches:
            return jsonify({"error": "No branches found"}), 404

        nearest = None
        min_distance = float('inf')
        
        for branch in branches:
            distance = haversine_distance(
                geo_data['latitude'],
                geo_data['longitude'],
                branch.latitude,
                branch.longitude
            )
            if distance < min_distance:
                min_distance = distance
                nearest = branch

        # Se regresa en formato JSON la sucursal más cercana y la distancia
        return jsonify({
            "nearest_branch": {
                "id": nearest.id,
                "name": nearest.name,
                "address": nearest.address,
                "coordinates": {
                    "latitude": nearest.latitude,
                    "longitude": nearest.longitude
                }
            },
            "distance_km": round(min_distance, 2),
            "customer_location": {
                "neighborhood": geo_data.get('neighborhood', ''),
                "full_address": geo_data['formatted_address'],
                "coordinates": {
                    "latitude": geo_data['latitude'],
                    "longitude": geo_data['longitude']
                }
            }
        })

    except Exception as e:
        app.logger.error(f"Error finding nearest branch: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Legado de la API para obtener la sucursal más cercana usando una cadena de dirección
@app.route('/api/branches/nearest_legacy', methods=['GET'])
def get_nearest_branch_legacy():
    address = request.args.get('address')
    motorbike_id = request.args.get('motorbike_id', type=int)
    
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    
    try:
        customer_loc = geocode_address(address)
        if not customer_loc:
            return jsonify({"error": "Could not geocode address"}), 400

        query = Branch.query
        if motorbike_id:
            query = query.filter_by(motorbike_id=motorbike_id)
        branches = query.all()
        
        if not branches:
            return jsonify({"error": "No branches found matching criteria"}), 404

        nearest = None
        min_distance = float('inf')
        
        # Calcular la distancia entre la sucursal y la ubicación del cliente 
        # Se considera la sucursal más cercana
        for branch in branches:
            distance = haversine_distance(
                customer_loc['latitude'],
                customer_loc['longitude'],
                branch.latitude,
                branch.longitude
            )
            if distance < min_distance:
                min_distance = distance
                nearest = branch

        return jsonify({
            "branch": nearest.to_dict(),
            "distance_km": round(min_distance, 2),
            "customer_location": customer_loc
        })
        
    except Exception as e:
        app.logger.error(f"Error in legacy nearest branch: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Se obtiene la lista de Motocicicletas disponibles
@app.route('/api/motorbikes', methods=['GET'])
def get_motorbikes():
    motorbikes = Motorbike.query.all()
    return jsonify([{
        'id': m.id,
        'brand': m.brand,
        'model': m.model,
        'color': m.color
    } for m in motorbikes])

# Se valida que la API esté funcionando
@app.route('/')
def home():
    return {"status": "OK", "message": "Flask backend is running"}