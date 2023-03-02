from fastapi import APIRouter, Depends,HTTPException, status
from schema import schemas
from setup import database
from sqlalchemy.orm import Session
from typing import List
from model import models

router = APIRouter()
get_db = database.get_db

@router.get('/room', response_model=List[schemas.Room], tags=['rooms'])
def get_rooms(db: Session = Depends(get_db)):
    room = db.query(models.Room).all()
    return room

@router.get('/room/{id}', response_model=schemas.Room, tags=['rooms'])
def get_room(id:int, db:Session=Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id==id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with the id {id} not found")
    return room

@router.put('/room/{id}',tags=['rooms'])
def update_room(request:schemas.Room, id:int, db:Session=Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id==id)
    if not room.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Room with the id {id} not found")
    room.update(request.dict(exclude_unset=False))
    db.commit()
    return {'message':f"Room with id {id} updated succesfully"}


@router.post('/room', response_model=schemas.Room, tags=['rooms'])
def create_room(request:schemas.Room, db: Session = Depends(get_db)):
    room = models.Room(**request.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.delete('/room/{id}',tags=['rooms'])
def destroy(id, db: Session=Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id==id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Admin with the id {id} not found")
    room.delete(synchronize_session=False)
    db.commit()
    return 'done'