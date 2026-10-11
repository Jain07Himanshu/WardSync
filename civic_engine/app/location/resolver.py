"""Location normalization, geocoding resolver, and spatial distance calculation."""

import math
import re
from typing import Optional, Tuple, Dict, Any


# Curated municipal registry of known localities, wards, and benchmark coordinates
MUMBAI_METRO_LOCATION_REGISTRY: Dict[str, Dict[str, Any]] = {
    "andheri west": {
        "normalized": "Andheri West, Mumbai",
        "ward": "K-West",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.1197,
        "longitude": 72.8468,
    },
    "andheri east": {
        "normalized": "Andheri East, Mumbai",
        "ward": "K-East",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.1136,
        "longitude": 72.8697,
    },
    "bandra west": {
        "normalized": "Bandra West, Mumbai",
        "ward": "H-West",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0596,
        "longitude": 72.8295,
    },
    "bandra east": {
        "normalized": "Bandra East, Mumbai",
        "ward": "H-East",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0626,
        "longitude": 72.8465,
    },
    "dadar": {
        "normalized": "Dadar, Mumbai",
        "ward": "G-North",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0178,
        "longitude": 72.8478,
    },
    "malad west": {
        "normalized": "Malad West, Mumbai",
        "ward": "P-North",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.1865,
        "longitude": 72.8375,
    },
    "milan subway": {
        "normalized": "Milan Subway, Santacruz West, Mumbai",
        "ward": "H-West",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0833,
        "longitude": 72.8367,
    },
    "hindmata": {
        "normalized": "Hindmata Junction, Dadar East, Mumbai",
        "ward": "F-South",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0094,
        "longitude": 72.8427,
    },
    "kurla": {
        "normalized": "Kurla West, Mumbai",
        "ward": "L Ward",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0726,
        "longitude": 72.8845,
    },
    "ghodbunder road": {
        "normalized": "Ghodbunder Road, Thane West",
        "ward": "Majiwada-Manpada Ward",
        "jurisdiction": "Thane Municipal Corporation (TMC)",
        "latitude": 19.2616,
        "longitude": 72.9667,
    },
    "vashi": {
        "normalized": "Vashi, Navi Mumbai",
        "ward": "Vashi Ward",
        "jurisdiction": "Navi Mumbai Municipal Corporation (NMMC)",
        "latitude": 19.0771,
        "longitude": 72.9986,
    },
    "borivali west": {
        "normalized": "Borivali West, Mumbai",
        "ward": "R-Central",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.2307,
        "longitude": 72.8567,
    },
    "worli": {
        "normalized": "Worli, Mumbai",
        "ward": "G-South",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0134,
        "longitude": 72.8154,
    },
    "powai": {
        "normalized": "Powai, Mumbai",
        "ward": "S Ward",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.1176,
        "longitude": 72.9060,
    },
    "ghatkopar": {
        "normalized": "Ghatkopar East, Mumbai",
        "ward": "N Ward",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 19.0860,
        "longitude": 72.9080,
    },
    "colaba": {
        "normalized": "Colaba, Mumbai",
        "ward": "A Ward",
        "jurisdiction": "Brihanmumbai Municipal Corporation (BMC)",
        "latitude": 18.9067,
        "longitude": 72.8147,
    },
}


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on Earth in kilometers."""
    r = 6371.0  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


def resolve_location(raw_text: Optional[str]) -> Dict[str, Any]:
    """
    Resolve raw location string to normalized name, ward, civic jurisdiction,
    and verified coordinates. If uncertain, leaves coordinates null.
    """
    if not raw_text or not raw_text.strip():
        return {
            "normalized_location": "Unspecified Urban Locality",
            "ward_zone": None,
            "jurisdiction_name": "Municipal Corporation Jurisdiction",
            "latitude": None,
            "longitude": None,
            "is_geocoded": False,
        }

    clean = raw_text.lower().strip()

    # Exact or substring match in registry
    for key, data in MUMBAI_METRO_LOCATION_REGISTRY.items():
        if key in clean:
            return {
                "normalized_location": data["normalized"],
                "ward_zone": data["ward"],
                "jurisdiction_name": data["jurisdiction"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "is_geocoded": True,
            }

    # Fallback to normalized title-case string without inventing fake coordinates
    capitalized = " ".join(w.capitalize() for w in re.split(r"[\s,]+", raw_text) if w)
    return {
        "normalized_location": capitalized,
        "ward_zone": "General Ward Jurisdiction",
        "jurisdiction_name": "Local Civic Authority",
        "latitude": None,
        "longitude": None,
        "is_geocoded": False,
    }
