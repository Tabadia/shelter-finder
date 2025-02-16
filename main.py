from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
from models import Shelter, User, Reservation, ShelterPost, ShelterUpdate, UserUpdate, ReservationUpdate, Location, QueueItem, ClientPost, Client, ClientLogin
from aws import get_all_shelters, get_my_shelters, get_shelter_by_id, post_shelter, get_all_users, post_user, get_all_reservations, get_reservation_by_id, post_reservation, update_shelter, check_client_login, del_shelter, find_user_by_shelter_id
from distance import get_travel_time, convert_duration_to_minutes
from summary import gen_summary
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# address = ""


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
    #shelter.summary = gen_summary(shelter.name, shelter.queue, shelter.curr_cap, shelter.capacity, shelter.resources, shelter.type)
    print(shelter)
    print("\n...................\n")
    print(update_shelter(shelter))
    return {"message": "Added to queue successfully",
    "count": queue_count(shelter)
    }

def queue_count(shelter):
    count = 0
    print(shelter.queue)
    for s in shelter.queue:
        count += s.num_people

    return count

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
    shelter = get_shelter_by_id(reservation.shelter_id)
    shelter = Shelter(**shelter)
    for s in shelter.queue:
        if reservation.phone_number == s.phone_number:
            return {"message": "Error: phone number already added"}
    # print(reservation.)
    #is phone legit
    # if not raise http error 404
    #print(queue_count(reservation))
    return add_to_queue(reservation.shelter_id, reservation.phone_number, reservation.num_people, reservation.name)

@app.post("/check-in/{shelter_id}/{phone_number}")
async def check_in_shelter(shelter_id: str, phone_number: str):
    shelter = get_shelter_by_id(shelter_id)
    shelter_obj = Shelter(**shelter)
    
    for q in shelter_obj.queue:
        if q.phone_number == phone_number:
            print(q)
            q.check_in = True
            shelter_obj.curr_cap += q.num_people
            print(shelter_obj)
            return update_shelter(shelter_obj)

    return {"message": "Reservation not found"}

@app.delete("/check-in/{shelter_id}/{phone_number}")
async def check_in_shelter(shelter_id: str, phone_number: str):
    shelter = get_shelter_by_id(shelter_id)
    shelter_obj = Shelter(**shelter)
    
    for q in shelter_obj.queue:
        if q.phone_number == phone_number:
            shelter_obj.queue.remove(q)
            return update_shelter(shelter_obj)

    return {"message": "Reservation not found"}



# Shelter Endpoints
@app.get("/shelters/", response_model=List[Shelter])
async def read_shelters():
    return get_all_shelters()

@app.get("/shelters/owner/{owner_username}", response_model=List[Shelter])
async def my_shelters(owner_username: str):
    return get_my_shelters(owner_username)

@app.get("/shelters/{shelter_id}", response_model=Shelter)
async def read_shelter(shelter_id: str):
    ret = get_shelter_by_id(shelter_id)
    if not ret:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return ret

@app.get("/shelters/queue/{shelter_id}")
async def shelter_queue(shelter_id: str):
    ret = get_shelter_by_id(shelter_id)
    qu, check_in = [], []
    for q in ret["queue"]:
        if q["check_in"]:
            check_in.append(q)
        else:
            qu.append(q)
    if not ret:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return qu, check_in

@app.post("/shelters/", response_model=Shelter)
async def create_shelter(shelter: ShelterPost):
    return post_shelter(shelter)

@app.delete("/shelters/{shelter_id}")
async def delete_shelter(shelter_id: str):
    print(shelter_id)
    del_shelter(shelter_id)
    res = find_user_by_shelter_id(shelter_id)
    print(res)

# User Endpoints
@app.get("/users/", response_model=List[Client])
async def read_users():
    return get_all_users()


@app.post("/api/client/signup")
async def create_user(user: ClientPost):
    ret = post_user(user)
    if ret == 0:
        return {"status": "0"} # user created
    else:
        return {"status": "1"} # user already exists


@app.post("/api/client/login/")
async def client_login(clientLogin: ClientLogin):
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


@app.get("/location/{lat},{lon}")
async def get_location(lat: float, lon: float):
    start_time = time.time()
    
    shelter_data = get_all_shelters()
    #print(f"Checkpoint 1: Got all shelter data | Time elapsed: {time.time() - start_time:.2f} seconds")

    for idx, s in enumerate(shelter_data):
        loop_start_time = time.time()
        #print(f"Beginning of getting times for shelter {idx + 1} | Time elapsed: {time.time() - start_time:.2f} seconds")
        
        time_taken = get_travel_time(lat, lon, s["address"])
        #print(f"Checkpoint: Shelter {idx + 1} time found | Time elapsed: {time.time() - start_time:.2f} seconds | Time for this shelter: {time.time() - loop_start_time:.2f} seconds")
        
        s["time"] = time_taken
        #print(f"Checkpoint: Shelter {idx + 1} time updated | Time elapsed: {time.time() - start_time:.2f} seconds")

    #print(f"Last checkpoint | Total execution time: {time.time() - start_time:.2f} seconds")

    return shelter_data
    
@app.get("/view-queue/{shelter}")
async def view_queue(shelter):
    #returns the total number of people currently in a reservation and AI generated summary
    current_num_queue = queue_count(shelter)
    open_seats_left = shelter.capacity - shelter.curr_cap
    total_queue = open_seats_left - current_num_queue
    summary = gen_summary(shelter.name, shelter.queue, shelter.curr_cap, shelter.capacity, shelter.resources, shelter.type)
    return current_num_queue, open_seats_left, total_queue, summary 
