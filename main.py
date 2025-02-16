from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
from models import Shelter, User, Reservation, ShelterPost, ShelterUpdate, UserUpdate, ReservationUpdate, Location
from data import shelters, users, reservations
from distance import geocode, get_radar_time
from aws import get_all_shelters, get_my_shelters, get_shelter_by_id, post_shelter, get_all_users, post_user, \
    get_all_reservations, get_reservation_by_id, post_reservation
# from user.distance import reverse_geocode


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

address = ""



# Shelter Endpoints
@app.get("/")
async def read_root():
    return FileResponse("templates/index.html")


@app.get("/client-login")
async def get_client():
    return FileResponse("templates/client-login.html")

@app.get("/client")
async def get_client():
    return FileResponse("templates/client.html")

@app.get("/add-shelter")
async def get_client():
    return FileResponse("templates/add-shelter.html")



@app.post("/reserve/{shelter_id},{phone_number},{num_people}")
async def reserve_shelter(shelter_id: int, phone_number: int, num_people: int):
    return {"message": "Reservation created successfully"}

# Shelter Endpoints
@app.get("/shelters/", response_model=List[Shelter])
async def read_shelters():
    return get_all_shelters()

@app.get("/shelters/owner/{owner_id}", response_model=List[Shelter])
async def read_shelters(owner_id: int):
    print("in shelters onwer:", owner_id)
    return get_my_shelters(owner_id)

@app.get("/shelters/{shelter_id}", response_model=Shelter)
async def read_shelter(shelter_id: str):
    ret = get_shelter_by_id(shelter_id)
    if not ret:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return ret

@app.post("/shelters/", response_model=Shelter)
async def create_shelter(shelter: ShelterPost):
    return post_shelter(shelter)

@app.put("/shelters/{shelter_id}", response_model=Shelter)
async def update_shelter(shelter_id: str, shelter: ShelterUpdate):
    return update_shelter(shelter_id, shelter.dict())

@app.delete("/shelters/{shelter_id}")
async def delete_shelter(shelter_id: str):
    delete_shelter(shelter_id)
    return {"message": "Shelter deleted successfully"}

# User Endpoints
@app.get("/users/", response_model=List[User])
async def read_users():
    return get_all_users()

# @app.get("/users/{user_id}", response_model=User)
# async def read_user(user_id: int):
#     ret = get_user_by_id(user_id)
#     if not ret:
#         raise HTTPException(status_code=404, detail="User not found")
#     return ret

@app.post("/users/", response_model=User)
async def create_user(user: User):
    return post_user(user)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    return update_user(user_id, user.dict())

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    delete_user(user_id)
    return {"message": "User deleted successfully"}

# Reservation Endpoints
@app.get("/reservations/", response_model=List[Reservation])
async def read_reservations():
    return get_all_reservations()

@app.get("/reservations/{reservation_id}", response_model=Reservation)
async def read_reservation(reservation_id: int):
    ret = get_reservation_by_id(reservation_id)
    if not ret:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return ret

@app.post("/reservations/", response_model=Reservation)
async def create_reservation(reservation: Reservation):
    return post_reservation(reservation)

@app.put("/reservations/{reservation_id}", response_model=Reservation)
async def update_reservation(reservation_id: int, reservation: ReservationUpdate):
    return update_reservation(reservation_id, reservation.dict())

@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    delete_reservation(reservation_id)
    return {"message": "Reservation deleted successfully"}

# Live Headcount Endpoint
@app.get("/shelters/{shelter_id}/headcount")
async def get_headcount(shelter_id: int):
    # This is a placeholder for calculating the headcount based on reservations
    # For simplicity, it returns a dummy value
    return {"headcount": 10}

@app.get("/shelters/{shelter_id}/queue")
async def get_headcount(shelter_id: int):
    # This is a placeholder for calculating the queue based on reservations
    # For simplicity, it returns a dummy value
    return {"queue": 10}

@app.get("/location/{lat},{lon}")
async def get_location(lat: float, lon: float):
    print(lat, lon)
    shelter_data = get_all_shelters()

    for s in shelter_data:
        client_lat, client_lon = geocode(s["address"])
        distance = get_radar_time()
    print(shelter_data)
    return {"shelters": shelter_data}

