from pydantic import BaseModel
from typing import Optional, List

class Resources(BaseModel):
    first_aid: bool
    food: bool
    
    
class QueueItem(BaseModel):
    name: str
    phone_number: str
    num_people: int
    check_in: bool

## data models
class Shelter(BaseModel):
    ShelterID: str #     shelter_id = str(uuid.uuid4()) generate the id when creating the shelter
    name: str
    address: str
    capacity: int
    curr_cap: int
    queue: List[QueueItem]
    desc: str
    verif: bool
    type: str
    resources: str
    summary: str
    # time: int
    

class Client(BaseModel):
    id: str
    username: str
    password: str
    shelters_ids: List[str]

class User(BaseModel):
    id: int
    username: str  
    password: str
    shelter_ids: List[str]

class Reservation(BaseModel):
    id: int
    user_id: int # tie this into a user
    shelter_id: int
    start_date: str
    end_date: str
    f_size: int
    
class ClientPost(BaseModel):
    id: Optional[str]
    username: str
    password: str
    shelters_ids: Optional[List[str]] = []
    
    
class ClientLogin(BaseModel):
    username: str
    password: str

class ShelterPost(BaseModel):
    ShelterID: Optional[str]
    name: str
    address: str
    capacity: int
    queue: Optional[List[List[str]]] = []
    desc: str
    type: str
    verif: Optional[bool]
    resources: str

class ShelterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    capacity: Optional[int] = None
    queue: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class ReservationUpdate(BaseModel):
    user_id: Optional[int] = None
    shelter_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Location(BaseModel):
    lat: float
    lon: float
