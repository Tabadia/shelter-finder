## dummy data
shelters = [
    {"id": 1, "name": "Shelter 1", "address": "123 Main St", "capacity": 50, "queue": 0, "description": {str}, "verification": {bool}},
    {"id": 2, "name": "Shelter 2", "address": "456 Elm St", "capacity": 75, "queue": 0, "description": {str}, "verification": {bool}},
]

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"},
]

reservations = [
    {"id": 1, "user_id": 1, "shelter_id": 1, "start_date": "2023-01-01", "end_date": "2023-01-05"},
    {"id": 2, "user_id": 2, "shelter_id": 2, "start_date": "2023-01-10", "end_date": "2023-01-15"},
]
