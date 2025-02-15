from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
from models import Shelter, User, Reservation, ShelterUpdate, UserUpdate, ReservationUpdate
from data import shelters, users, reservations
from aws import get_all_shelters


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("templates/index.html")

# Dummy in-memory data store
shelter_data = shelters
user_data = users
reservation_data = reservations

# Shelter Endpoints
@app.get("/shelters/", response_model=List[Shelter])
async def read_shelters():
    return get_all_shelters()

@app.get("/shelters/{shelter_id}", response_model=Shelter)
async def read_shelter(shelter_id: int):
    for shelter in shelter_data:
        if shelter["id"] == shelter_id:
            return shelter
    raise HTTPException(status_code=404, detail="Shelter not found")

@app.post("/shelters/", response_model=Shelter)
async def create_shelter(shelter: Shelter):
    shelter_data.append(shelter.dict())
    return shelter

@app.put("/shelters/{shelter_id}", response_model=Shelter)
async def update_shelter(shelter_id: int, shelter: ShelterUpdate):
    for s in shelter_data:
        if s["id"] == shelter_id:
            s["name"] = shelter.name if shelter.name else s["name"]
            s["address"] = shelter.address if shelter.address else s["address"]
            s["capacity"] = shelter.capacity if shelter.capacity else s["capacity"]
            return s
    raise HTTPException(status_code=404, detail="Shelter not found")

@app.delete("/shelters/{shelter_id}")
async def delete_shelter(shelter_id: int):
    for s in shelter_data:
        if s["id"] == shelter_id:
            shelter_data.remove(s)
            return {"message": "Shelter deleted successfully"}
    raise HTTPException(status_code=404, detail="Shelter not found")

# User Endpoints
@app.get("/users/", response_model=List[User])
async def read_users():
    return user_data

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    for user in user_data:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/", response_model=User)
async def create_user(user: User):
    user_data.append(user.dict())
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    for u in user_data:
        if u["id"] == user_id:
            u["name"] = user.name if user.name else u["name"]
            u["email"] = user.email if user.email else u["email"]
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for u in user_data:
        if u["id"] == user_id:
            user_data.remove(u)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Reservation Endpoints
@app.get("/reservations/", response_model=List[Reservation])
async def read_reservations():
    return reservation_data

@app.get("/reservations/{reservation_id}", response_model=Reservation)
async def read_reservation(reservation_id: int):
    for reservation in reservation_data:
        if reservation["id"] == reservation_id:
            return reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

@app.post("/reservations/", response_model=Reservation)
async def create_reservation(reservation: Reservation):
    reservation_data.append(reservation.dict())
    return reservation

@app.put("/reservations/{reservation_id}", response_model=Reservation)
async def update_reservation(reservation_id: int, reservation: ReservationUpdate):
    for r in reservation_data:
        if r["id"] == reservation_id:
            r["user_id"] = reservation.user_id if reservation.user_id else r["user_id"]
            r["shelter_id"] = reservation.shelter_id if reservation.shelter_id else r["shelter_id"]
            r["start_date"] = reservation.start_date if reservation.start_date else r["start_date"]
            r["end_date"] = reservation.end_date if reservation.end_date else r["end_date"]
            return r
    raise HTTPException(status_code=404, detail="Reservation not found")

@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    for r in reservation_data:
        if r["id"] == reservation_id:
            reservation_data.remove(r)
            return {"message": "Reservation deleted successfully"}
    raise HTTPException(status_code=404, detail="Reservation not found")

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




# @app.post("/items")
# def create_item(item: Item):
#     if item.text is None:
#         raise HTTPException(status_code=400, detail="text is a required field")
#     items.append(item)
#     return items



# @app.get("/items/{item_id}", response_model=Item)
# def read_item(item_id: int) -> Item:
#     if 0 <= item_id < len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

# @app.delete("/items/{item_id}", response_model=Item)
# def delete_item(item_id: int) -> Item:
#     if 0 <= item_id < len(items):
#         return items.pop(item_id)
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    
# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: int, item: Item) -> Item:
#     if 0 <= item_id < len(items):
#         items[item_id] = item
#         return item
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


