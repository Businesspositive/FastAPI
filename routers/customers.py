from fastapi import APIRouter, Depends,HTTPException, status

from schema import schemas
from setup import database
from sqlalchemy.orm import Session
from typing import List
from model import models

router = APIRouter()
get_db = database.get_db

@router.get('/customer', response_model=List[schemas.Customer], tags=['customers'])
def get_users(db: Session = Depends(get_db)):
    customer = db.query(models.Customer).all()
    return customer

@router.get('/customer/{id}', response_model=schemas.Customer, tags=['customers'])
def get_customer(id:int, db:Session=Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id==id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with the id {id} not found")
    return customer

@router.put('/customer/{id}',tags=['customers'])
def update_customer(request:schemas.Customer, id:int, db:Session=Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id==id)
    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    customer.update(request.dict(exclude_unset=False))
    db.commit()
    return {'message':f"Customer with id {id} updated succesfully"}


@router.post('/customer', response_model=schemas.Customer, tags=['customers'])
def create_customer(request:schemas.Customer, db: Session = Depends(get_db)):
    new_customer = models.Customer(**request.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.delete('/customer/{id}',tags=['customers'])
def destroy(id, db: Session=Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id==id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with the id {id} not found")
    customer.delete(synchronize_session=False)
    db.commit()
    return 'done'