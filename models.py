from pydantic import BaseModel
from typing import Optional, List

class Resources(BaseModel):
    first_aid: bool
    food: bool


class Reservation(BaseModel):
    shelter_id: str
    phone_number: str
    num_people: int
    name: str
    
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
    
class ShelterPost(BaseModel):
    ShelterID: Optional[str]
    name: str
    address: str
    capacity: int
    curr_cap: int
    queue: Optional[List[List[str]]] = []
    desc: str
    type: str
    curr_cap: Optional[int] = 0
    verif: Optional[bool]
    resources: str
    summary: Optional[str]
    
    owner_username: str

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
    
class ClientPost(BaseModel):
    id: Optional[str]
    username: str
    password: str
    shelters_ids: Optional[List[str]] = []
    
    
class ClientLogin(BaseModel):
    username: str
    password: str


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
