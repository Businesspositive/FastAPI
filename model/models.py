from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary, Float
from sqlalchemy.orm import relationship

from setup.database import Base

class UserNew(Base):
    __tablename__ = "myusers"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    user_name= Column(String)
    email= Column(String)
    email_verify = Column(String)
    password= Column(String)

    customers = relationship("Customer", back_populates="user")
    staffs = relationship("Staff", back_populates="user")
    admin = relationship("Admin", back_populates="user")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    name= Column(String)
    mobile_no= Column(String)
    mobile_verify = Column(String)
    created_at= Column(String)
    updated_at= Column(String)
    dob = Column(String)
    active= Column(String)
    user_id = Column(Integer, ForeignKey("myusers.id"))
                     
    user = relationship("UserNew", back_populates="customers")
    bookings = relationship("Booking", back_populates="customers")

class Staff(Base):
    __tablename__ = "staffs"

    staff_id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    name= Column(String)
    mobile_no= Column(String)
    mobile_verify = Column(String)
    rating = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    created_at= Column(String)
    updated_at= Column(String)
    user_id = Column(Integer, ForeignKey("myusers.id"))
                     
    user = relationship("UserNew", back_populates="staffs")
    hotels = relationship("Hotel", back_populates="staffs")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    name= Column(String)
    mobile_no= Column(String)
    mobile_verify = Column(String)
    created_at= Column(String)
    updated_at= Column(String)
    dob = Column(String)
    active= Column(String)
    user_id = Column(Integer, ForeignKey("myusers.id"))

    user = relationship("UserNew", back_populates="admin")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    hotel_name = Column(String)
    location = Column(String)
    state = Column(String)
    rating = Column(Integer)
    hotel_image = Column(LargeBinary)
    gym_available = Column(Boolean)
    food_available = Column(Boolean)
    allow_booking = Column(Boolean)


    staffs = relationship("Staff", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotels")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_type = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    room_price = Column(Float)
    rating = Column(Integer)
    image_link = Column(String)
    room_no = Column(Integer)

    hotels = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="rooms")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    room_id= Column(Integer, ForeignKey("rooms.id"))
    customer_id= Column(Integer, ForeignKey("customers.id"))
    check_in_date = Column(String)
    check_out_date= Column(String)
    checks_complete = Column(Boolean)
    total_price = Column(Float)

    customers = relationship("Customer", back_populates="bookings")
    rooms = relationship("Room", back_populates="bookings")
    payments = relationship("Payment", back_populates="bookings")
    ratings = relationship("Rating", back_populates="bookings")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    booking_id= Column(Integer, ForeignKey("bookings.id"))
    amount= Column(Float)
    created_at= Column(String)
    email = Column(String)
    status = Column(Boolean)
    notes = Column(String)

    bookings = relationship("Booking", back_populates="payments")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True) #relation with Customer,Staff. and Admin id field
    rating = Column(String)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    created_at = Column(String)

    updated_at = Column(String)
    comment = Column(String)

    bookings = relationship("Booking", back_populates="ratings")