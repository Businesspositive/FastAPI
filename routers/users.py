from fastapi import APIRouter, Depends,HTTPException, status

from schema import schemas
from setup import database
from sqlalchemy.orm import Session
from typing import List
from model import models

router = APIRouter()
get_db = database.get_db

@router.get('/user', response_model=List[schemas.UserNew], tags=['users'])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.UserNew).all()
    return user

@router.get('/user/{id}', response_model=schemas.UserNew, tags=['users'])
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.UserNew).filter(models.UserNew.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    return user

@router.put('/user/{id}',tags=['users'])
def update_user(request:schemas.UserNew, id:int, db:Session=Depends(get_db)):
    user = db.query(models.UserNew).filter(models.UserNew.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    user.update(request.dict(exclude_unset=False))
    db.commit()
    # updated = db.query(models.UserNew).filter(models.UserNew.id==id)
    return {'message':f"user with id {id} updated succesfully"}


@router.post('/user', response_model=schemas.UserNew, tags=['users'])
def create_user(request:schemas.UserNew, db: Session = Depends(get_db)):
    new_user = models.UserNew(id = request.id,user_name = request.user_name, email = request.email, email_verify = request.email_verify, password = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete('/user/{id}',tags=['users'])
def destroy(id, db: Session=Depends(get_db)):
    user = db.query(models.UserNew).filter(models.UserNew.id==id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with the id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return 'done'

