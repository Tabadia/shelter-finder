from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
from models import Shelter, User, Reservation, ShelterPost, ShelterUpdate, UserUpdate, ReservationUpdate, Location, QueueItem, ClientPost, Client, ClientLogin
from data import shelters, users, reservations
from aws import get_all_shelters, get_my_shelters, get_shelter_by_id, post_shelter, get_all_users, post_user, get_all_reservations, get_reservation_by_id, post_reservation, update_shelter, check_client_login
from distance import get_radar_time, geocode, convert_duration_to_minutes
from summary import gen_summary

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

@app.get("/client-signup")
async def get_client():
    return FileResponse("templates/signup.html")

@app.get("/client-dashboard")
async def get_client():
    return FileResponse("templates/client-dashboard.html")

@app.get("/add-shelter")
async def get_client():
    return FileResponse("templates/add-shelter.html")

# def add_to_queue(shelter, phone_number, num_people, name):




def add_to_queue(shelter_id, phone_number, num_people, name):
    reservation = QueueItem(
        name=name,
        phone_number=phone_number,
        num_people=num_people,
        check_in=False
    )
    shelter_data = get_shelter_by_id(shelter_id)
    shelter = Shelter(**shelter_data)
    shelter.queue.append(reservation)
    # move to where user is checked in
    if shelter.curr_cap == shelter.capacity:
        raise HTTPException(status_code=400, detailE="Shelter is full")
    shelter.summary = gen_summary(shelter.name, shelter.queue, shelter.curr_cap, shelter.capacity, shelter.resources, shelter.type)
    print(update_shelter(shelter))
    print(queue_count(shelter))
    return {"message": "Added to queue successfully"}

def queue_count(shelter):
    return len(shelter.queue)


# should be ran on frontend clientside
def check_in(shelter, phone_number, num_people):
    for q in shelter.queue:
        if q["phone_number"] == phone_number:
            q["check_in"] = True  # Fixed assignment
            q.curr_cap += num_people
            return {"message": "Check-in successful", "reservation": q}
    return {"error": "Reservation not found"}

@app.post("/reserve")
async def reserve_shelter(reservation: Reservation):
    print(reservation.dict())
    # print(reservation.)
    #is phone legit
    # if not raise http error 404
    #print(queue_count(reservation))
    return add_to_queue(reservation.shelter_id, reservation.phone_number, reservation.num_people, reservation.name)


# Shelter Endpoints
@app.get("/shelters/", response_model=List[Shelter])
async def read_shelters():
    return get_all_shelters()

@app.get("/shelters/owner/{owner_username}", response_model=List[Shelter])
async def my_shelters(owner_username: str):
    print("in shelters onwer:", owner_username)
    return get_my_shelters(owner_username)

@app.get("/shelters/{shelter_id}", response_model=Shelter)
async def read_shelter(shelter_id: str):
    ret = get_shelter_by_id(shelter_id)
    if not ret:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return ret

@app.post("/shelters/", response_model=Shelter)
async def create_shelter(shelter: ShelterPost):
    return post_shelter(shelter)

# @app.put("/shelters/{shelter_id}", response_model=Shelter)
# async def update_shelter(shelter_id: str, shelter: ShelterUpdate):
#     return update_shelter(shelter_id, shelter.dict())

@app.delete("/shelters/{shelter_id}")
async def delete_shelter(shelter_id: str):
    delete_shelter(shelter_id)
    return {"message": "Shelter deleted successfully"}

# User Endpoints
@app.get("/users/", response_model=List[Client])
async def read_users():
    return get_all_users()

# @app.get("/users/{username}", response_model=Client)
# async def get_user_by_username(username: str):
#     ret = get_user_by_username(username)
#     if not ret:
#         raise HTTPException(status_code=404, detail="User not found")
#     return ret

# @app.get("/users/{user_id}", response_model=User)
# async def read_user(user_id: int):
#     ret = get_user_by_id(user_id)
#     if not ret:
#         raise HTTPException(status_code=404, detail="User not found")
#     return ret

@app.post("/users/", response_model=Client)
async def create_user(user: ClientPost):
    return post_user(user)


@app.post("/api/client/login/")
async def client_login(clientLogin: ClientLogin):
    print('debug:', clientLogin)
    ret = check_client_login(clientLogin)
    if ret == 0:
       return {"status": "0"} # valid login
    if ret == 1:
        return {"status": "1"} # invalid login
    if ret == 2:
       return {"status": "2"} # user not found

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    return update_user(user_id, user.dict())

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    delete_user(user_id)
    return {"message": "User deleted successfully"}

# Reservation Endpoints
# @app.get("/reservations/", response_model=List[Reservation])
# async def read_reservations():
#     return get_all_reservations()

# @app.get("/reservations/{reservation_id}", response_model=Reservation)
# async def read_reservation(reservation_id: int):
#     ret = get_reservation_by_id(reservation_id)
#     if not ret:
#         raise HTTPException(status_code=404, detail="Reservation not found")
#     return ret

# @app.post("/reservations/", response_model=Reservation)
# async def create_reservation(reservation: Reservation):
#     return post_reservation(reservation)

# @app.put("/reservations/{reservation_id}", response_model=Reservation)
# async def update_reservation(reservation_id: int, reservation: ReservationUpdate):
#     return update_reservation(reservation_id, reservation.dict())

# @app.delete("/reservations/{reservation_id}")
# async def delete_reservation(reservation_id: int):
#     delete_reservation(reservation_id)
#     return {"message": "Reservation deleted successfully"}

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
    shelter_data = get_all_shelters()
    for s in shelter_data:
        time = get_radar_time(lat, lon, s["address"])
        s["time"] = time
    
    return shelter_data
    

