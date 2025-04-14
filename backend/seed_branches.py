import os
import sys
from dotenv import load_dotenv
import requests

# Se añade el directorio padre al path para poder importar el paquete
# Esto es necesario si el script se ejecuta desde un directorio diferente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from backend import app, db
from backend.models import Branch, Motorbike

load_dotenv()

# Se definen las sucursales de las ciudades de Mexico, Queretaro y Estado de Mexico
CITY_BRANCHES = [
    # Ciudad de Mexico
    {
        "name": "KTM Satelite Ferbel",
        "street": "Blvd. Manuel Avila Camacho",
        "number": "1920",
        "neighborhood": "Naucalpan de Juarez",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "53100",
        "motorbike_id": 2  # KTM 390 Duke
    },
    {
        "name": "Hiperbikes Capital",
        "street": "Blvd. Adolfo López Mateos",
        "number": "1347",
        "neighborhood": "Santa Maria",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "01420",
        "motorbike_id": 2  # KTM 390 Duke
    },
    {
        "name": "Hiperbikes Ajusco",
        "street": "CARRETERA PICACHO AJUSCO",
        "number": "752",
        "neighborhood": "Heroes de Padierna",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "14200",
        "motorbike_id": 2  # KTM 390 Duke
    },
    {
        "name": "KTM Coapa Ferbel",
        "street": "Avenida Canal de Miramontes",
        "number": "3000",
        "neighborhood": "Coyoacan",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "04800",
        "motorbike_id": 2  # KTM 390 Duke
    },
    {
        "name": "FAST Yamaha Ejercito Nacional",
        "street": "Av. Ejército Nacional",
        "number": "109",
        "neighborhood": "Veronica Anzures",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "11300",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "FAST Yamaha Buenavista",
        "street": "Insurgentes Norte",
        "number": "136",
        "neighborhood": "Santa María la Rivera",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "06350",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "FAST Yamaha Donatello",
        "street": "Av. Patriotismo",
        "number": "839",
        "neighborhood": "Insurgentes Mixcoac",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "03920",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "FAST Yamaha Vallejo",
        "street": "Av. Vallejo",
        "number": "100",
        "neighborhood": "Vallejo",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "02300",
        "motorbike_id": 1  # Yamaha R3
    },
    { #skipped
        "name": "FAST Yamaha Maximotos",
        "street": "Periférico Sur",
        "number": "5932",
        "neighborhood": "Cantera Puente de Piedra",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "14040",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Yamaha Miramontes",
        "street": "Canal de Miramontes",
        "number": "120",
        "neighborhood": "Coapa",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "14300",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Moto Azcapotzalco",
        "street": "Esperanza",
        "number": "11",
        "neighborhood": "Azcapotzalco",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "02000",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Motos Iztapalapa Constitución",
        "street": "Calzada Ermita Iztapalapa",
        "number": "2202",
        "neighborhood": "Iztapalapa",
        "city": "Ciudad de Mexico",
        "state": "CDMX", 
        "country": "Mexico",
        "zipcode": "09260",
        "motorbike_id": 1  # Yamaha R3
    },
    # Queretaro
    {
        "name": "Yamaha Juriquilla",
        "street": "Av Paseo de la República",
        "number": "10874C",
        "neighborhood": "Ejido el Salitre",
        "city": "Santiago de Querétaro",
        "state": "Qro", 
        "country": "Mexico",
        "zipcode": "76127",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Motocicletas Yamaha",
        "street": "Blvd. Bernardo Quintana",
        "number": "181",
        "neighborhood": "Fracc. Los Arcos",
        "city": "Santiago de Querétaro",
        "state": "Qro", 
        "country": "Mexico",
        "zipcode": "76060",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Moto Plaza Querétaro",
        "street": "Prol. Bernardo Quintana",
        "number": "209",
        "neighborhood": "Loma Dorada",
        "city": "Santiago de Querétaro",
        "state": "Qro", 
        "country": "Mexico",
        "zipcode": "76060",
        "motorbike_id": 2  # KTM 390 Duke
    },
    # Estado de Mexico
    {
        "name": "Yamaha Motos del centro",
        "street": "Av. Valle de Bravo",
        "number": "73",
        "neighborhood": "La Romana",
        "city": "Tlalnepantla",
        "state": "Edomex", 
        "country": "Mexico",
        "zipcode": "54030",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Yamaha Tlapanaloya",
        "street": "Av. Manzanares",
        "number": "SN",
        "neighborhood": "Francisco I Madero",
        "city": "Tlapanaloya",
        "state": "Edomex", 
        "country": "Mexico",
        "zipcode": "55653",
        "motorbike_id": 1  # Yamaha R3
    },
    {
        "name": "Jass motos Yamaha",
        "street": "Del Lago",
        "number": "211",
        "neighborhood": "Analco",
        "city": "Teoloyucan",
        "state": "Edomex", 
        "country": "Mexico",
        "zipcode": "54783",
        "motorbike_id": 1  # Yamaha R3
    },

    {
        "name": "KTM Toluca",
        "street": "Carr México - Toluca",
        "number": "47.5",
        "neighborhood": "Amomolulco",
        "city": "Lerma de Villada",
        "state": "Edomex", 
        "country": "Mexico",
        "zipcode": "52005",
        "motorbike_id": 2  # Duke 390
    },   
    {
        "name": "KTM Metepec",
        "street": "Leona Vicario",
        "number": "610",
        "neighborhood": "Coaxustenco",
        "city": " San Francisco Coaxusco",
        "state": "Edomex",
        "country": "Mexico",
        "zipcode": "52149",
        "motorbike_id": 2  # Duke 390
    }
]

def geocode_address(address_components):
    """Same geocoding function from your app.py"""
    params = {
        'street': address_components['street'],
        'number': address_components['number'],
        'neighborhood': address_components['neighborhood'],
        'city': address_components['city'],
        'state': address_components['state'],
        'country': address_components['country'],
        'postalcode': address_components['zipcode'],
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'BranchSeeder/1.0'}
    
    try:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params=params,
            headers=headers,
            timeout=5
        )
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return {
                'latitude': float(data['lat']),
                'longitude': float(data['lon']),
                'formatted_address': data['display_name']
            }
    except Exception as e:
        print(f"Geocoding failed for {address_components}: {str(e)}")
    return None

def seed_branches():
    with app.app_context():
        print("Seeding branches...")
        
        for branch_data in CITY_BRANCHES:
            # Geocode each address
            geo_data = geocode_address(branch_data)
            if not geo_data:
                print(f"Skipping {branch_data['name']} - geocoding failed")
                continue
            
            # Create branch instance
            branch = Branch(
                name=branch_data['name'],
                address=geo_data['formatted_address'],
                latitude=geo_data['latitude'],
                longitude=geo_data['longitude'],
                motorbike_id=branch_data['motorbike_id']
            )
            
            db.session.add(branch)
            print(f"Added branch: {branch.name} at {branch.address}")
        
        db.session.commit()
        print("Branch seeding completed!")

if __name__ == '__main__':
    seed_branches()