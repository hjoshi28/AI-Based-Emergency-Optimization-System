"""
Sample City Data
Pre-built city graph with intersections, roads, hospitals, and ambulances.
Provides default data for the emergency dispatch system.
"""

import random
from models.city_graph import CityGraph
from models.hospital import Hospital
from models.ambulance import Ambulance


def create_city_graph():
    """
    Create a sample city graph with 20 intersections and ~30 roads.
    The layout represents a realistic city grid with some diagonal roads.

    Returns:
        CityGraph: The constructed city graph.
    """
    city = CityGraph()

    # Add 20 intersection nodes with (x, y) coordinates
    intersections = {
        'A': (1, 8),   'B': (3, 9),   'C': (5, 9),   'D': (7, 8),
        'E': (1, 6),   'F': (3, 7),   'G': (5, 7),   'H': (7, 6),
        'I': (2, 5),   'J': (4, 5),   'K': (6, 5),   'L': (8, 5),
        'M': (1, 3),   'N': (3, 3),   'O': (5, 3),   'P': (7, 3),
        'Q': (2, 1),   'R': (4, 1),   'S': (6, 1),   'T': (8, 1),
    }

    for node_id, (x, y) in intersections.items():
        city.add_intersection(node_id, x, y)

    # Add roads (edges) with default traffic factor 1.0
    roads = [
        # Top row connections
        ('A', 'B'), ('B', 'C'), ('C', 'D'),
        # Upper middle connections
        ('E', 'F'), ('F', 'G'), ('G', 'H'),
        # Middle row connections
        ('I', 'J'), ('J', 'K'), ('K', 'L'),
        # Lower middle connections
        ('M', 'N'), ('N', 'O'), ('O', 'P'),
        # Bottom row connections
        ('Q', 'R'), ('R', 'S'), ('S', 'T'),
        # Vertical connections (left side)
        ('A', 'E'), ('E', 'I'), ('I', 'M'), ('M', 'Q'),
        # Vertical connections (center-left)
        ('B', 'F'), ('F', 'J'), ('J', 'N'), ('N', 'R'),
        # Vertical connections (center-right)
        ('C', 'G'), ('G', 'K'), ('K', 'O'), ('O', 'S'),
        # Vertical connections (right side)
        ('D', 'H'), ('H', 'L'), ('L', 'P'), ('P', 'T'),
        # Some diagonal connections for realism
        ('A', 'F'), ('F', 'K'), ('C', 'F'),
        ('I', 'N'), ('K', 'P'),
    ]

    for node1, node2 in roads:
        city.add_road(node1, node2, traffic_factor=1.0)

    return city


def create_hospitals():
    """
    Create sample hospitals at various locations in the city.

    capacity_limit is the maximum number of occupied beds a hospital accepts
    (90% of total beds here), so constraint C4 is independent of C1.

    Returns:
        list[Hospital]: List of hospital objects.
    """
    hospitals = [
        Hospital(
            name="City General Hospital",
            node='C',
            total_beds=50,
            available_beds=12,
            icu_available=True,
            doctors_available=8,
            capacity_limit=45
        ),
        Hospital(
            name="St. Mary's Medical Center",
            node='H',
            total_beds=30,
            available_beds=5,
            icu_available=True,
            doctors_available=4,
            capacity_limit=27
        ),
        Hospital(
            name="Emergency Care Hospital",
            node='N',
            total_beds=40,
            available_beds=15,
            icu_available=False,
            doctors_available=6,
            capacity_limit=36
        ),
        Hospital(
            name="National Trauma Center",
            node='P',
            total_beds=60,
            available_beds=20,
            icu_available=True,
            doctors_available=10,
            capacity_limit=54
        ),
        Hospital(
            name="Westside Clinic",
            node='E',
            total_beds=20,
            available_beds=3,
            icu_available=False,
            doctors_available=2,
            capacity_limit=18
        ),
    ]
    return hospitals


def create_ambulances():
    """
    Create sample ambulances at various locations.

    Returns:
        list[Ambulance]: List of ambulance objects.
    """
    ambulances = [
        Ambulance(ambulance_id="AMB-01", current_node='A', is_available=True, speed=60),
        Ambulance(ambulance_id="AMB-02", current_node='J', is_available=True, speed=55),
        Ambulance(ambulance_id="AMB-03", current_node='T', is_available=True, speed=65),
        Ambulance(ambulance_id="AMB-04", current_node='M', is_available=False, speed=60),
    ]
    return ambulances


def randomize_traffic(city_graph):
    """
    Randomize traffic conditions on all roads.
    Traffic factor ranges from 1.0 (clear) to 3.0 (heavy).

    Args:
        city_graph (CityGraph): The city graph to update.
    """
    for u, v, data in city_graph.get_edges():
        new_factor = round(random.uniform(1.0, 3.0), 1)
        city_graph.update_traffic(u, v, new_factor)


def get_emergency_scenarios():
    """
    Get predefined emergency scenarios for testing.

    Returns:
        list[dict]: List of emergency scenario dicts.
    """
    scenarios = [
        {
            "name": "Heart Attack at Intersection Q",
            "location": "Q",
            "severity": "Critical",
            "icu_required": True,
        },
        {
            "name": "Car Accident at Intersection G",
            "location": "G",
            "severity": "High",
            "icu_required": False,
        },
        {
            "name": "Fall Injury at Intersection L",
            "location": "L",
            "severity": "Medium",
            "icu_required": False,
        },
        {
            "name": "Stroke at Intersection A",
            "location": "A",
            "severity": "Critical",
            "icu_required": True,
        },
    ]
    return scenarios
