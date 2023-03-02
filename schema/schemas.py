from pydantic import BaseModel

class UserNew(BaseModel):
    id: int
    user_name: str
    email: str
    email_verify: str
    password: str

    class Config:
        orm_mode = True


class Customer(BaseModel):
    id: int
    name: str
    mobile_no: str
    mobile_verify: str
    created_at: str
    updated_at: str
    dob: str
    active: str

    class Config:
        orm_mode = True

class Staff(BaseModel):
    id: int
    name: str
    mobile_no: str
    mobile_verify: str
    rating : int
    hotel_id: int #relation with id in Hotel
    created_at: str
    updated_at: str
    active: str


class Admin(BaseModel):
    id: int 
    name: str
    mobile_no: str
    mobile_verify: str
    created_at: str
    updated_at: str
    dob: str
    active: str

class Hotel(BaseModel):
    id: int #relation with Hotemid in Room and Staff
    hotel_name: str
    location: str
    state: str
    rating : int
    hotel_image: str #this can be a imagefield find out how include imagefield
    gym_available: bool
    food_available: bool
    allow_booking : bool

class Room(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    created_at: str
    updated_at: str
    room_price: float
    rating: int
    image_link: str
    room_no: int

class Booking(BaseModel):
    id: int
    room_id: int #relation with id from Room
    customer_id: int #relation with id from Customer table
    booking_start_date: str
    booking_end_date: str
    booking_status: str
    checks_complete: bool
    total_price: float

class Payment(BaseModel):
    id: int
    booking_id: int #relation with id from Booking table
    amount: float
    created_at: str
    email: str
    status: str
    notes: str

class Rating(BaseModel):
    id: int
    rating: int
    booking_id: int
    created_at: str
    updated_at: str
    comment: str