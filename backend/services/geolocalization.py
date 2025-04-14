import requests
from math import radians, sin, cos, sqrt, atan2
from backend.models import db, Branch
from flask import current_app
from time import sleep

# Constants
EARTH_RADIUS_KM = 6371.0
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def geocode_structured_address(address_components):
    """Enhanced with neighborhood support"""
    # Build the query prioritizing neighborhood
    query_parts = []
    if 'neighborhood' in address_components:
        query_parts.append(address_components['neighborhood'])
    if 'street' in address_components:
        query_parts.append(address_components['street'])
    if 'number' in address_components:
        query_parts.append(address_components['number'])
    
    params = {
        'q': ', '.join(filter(None, query_parts)),
        'city': address_components.get('city', ''),
        'state': address_components.get('state', ''),
        'country': address_components.get('country', ''),
        'postalcode': address_components.get('zipcode', ''),
        'format': 'json',
        'limit': 1,
        'addressdetails': 1  # Get more detailed address components
    }
    
    # Remove empty parameters
    params = {k: v for k, v in params.items() if v}
    
    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers={'User-Agent': 'MotorbikeFinder/1.0'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                result = data[0]
                return {
                    'latitude': float(result['lat']),
                    'longitude': float(result['lon']),
                    'formatted_address': result['display_name'],
                    'neighborhood': result.get('address', {}).get('suburb') or 
                                  result.get('address', {}).get('neighbourhood') or
                                  address_components.get('neighborhood', '')
                }
    except Exception as e:
        app.logger.error(f"Geocoding error: {str(e)}")
    
    return None

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return EARTH_RADIUS_KM * c

def find_nearest_branch(customer_address, motorbike_id=None):
    """Find the nearest branch matching criteria"""
    # Geocode customer address
    customer_loc = geocode_address(customer_address)
    if not customer_loc:
        raise ValueError("Could not geocode customer address")
    
    # Query branches (filter by motorbike if specified)
    query = Branch.query
    if motorbike_id:
        query = query.filter_by(motorbike_id=motorbike_id)
    branches = query.all()
    
    if not branches:
        raise ValueError("No branches found matching criteria")
    
    # Calculate distances
    nearest = None
    min_distance = float('inf')
    
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
    
    return {
        'branch': nearest,
        'distance_km': round(min_distance, 2),
        'customer_location': customer_loc
    }

def save_branch_with_geodata(branch_name, address, motorbike_id):
    """Save branch with geolocation data (unchanged)"""
    geo_data = geocode_address(address)
    if not geo_data:
        raise ValueError("Address geocoding failed")
    
    branch = Branch(
        name=branch_name,
        address=geo_data['formatted_address'],
        latitude=geo_data['latitude'],
        longitude=geo_data['longitude'],
        motorbike_id=motorbike_id
    )
    db.session.add(branch)
    db.session.commit()
    return branch