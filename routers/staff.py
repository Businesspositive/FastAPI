from fastapi import APIRouter, Depends,HTTPException, status
from schema import schemas
from setup import database
from sqlalchemy.orm import Session
from typing import List, Dict
from model import models

router = APIRouter()
get_db = database.get_db

@router.get('/staff', response_model=List[schemas.Staff], tags=['staffs'])
def get_staff(db: Session = Depends(get_db)):
    staff = db.query(models.Staff).all()
    return staff

@router.get('/staff/{id}', response_model=schemas.Staff, tags=['staffs'])
def get_staff(id:int, db:Session=Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.staff_id==id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"staff with the id {id} not found")
    return staff

@router.put('/staff/{id}',tags=['staffs'])
def update_staff(request:schemas.Staff, id:int, db:Session=Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.staff_id==id)
    if not staff.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Staff with the id {id} not found")
    staff.update(request.dict(exclude_unset=False))
    db.commit()
    return {'message':f"Staff with id {id} updated succesfully"}


@router.post('/staff', response_model=schemas.Staff, tags=['staffs'])
def create_staff(request:schemas.Staff, db: Session = Depends(get_db)):
    new_staff = models.Staff(**request.dict())
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    print(new_staff)
    return new_staff

@router.delete('/staff/{id}',tags=['staffs'])
def destroy(id, db: Session=Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.staff_id==id)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Staff with the id {id} not found")
    staff.delete(synchronize_session=False)
    db.commit()
    return 'done'