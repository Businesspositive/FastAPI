from fastapi import APIRouter, Depends,HTTPException, status
from schema import schemas
from setup import database
from sqlalchemy.orm import Session
from typing import List, Dict
from model import models

router = APIRouter()
get_db = database.get_db

@router.get('/admin', response_model=List[schemas.Admin], tags=['admins'])
def get_admin(db: Session = Depends(get_db)):
    admin = db.query(models.Admin).all()
    return admin

@router.get('/admin/{id}', response_model=schemas.Admin, tags=['admins'])
def get_admin(id:int, db:Session=Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id==id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin with the id {id} not found")
    return admin

@router.put('/admin/{id}',tags=['admins'])
def update_admin(request:schemas.Admin, id:int, db:Session=Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id==id)
    if not admin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin with the id {id} not found")
    admin.update(request.dict(exclude_unset=False))
    db.commit()
    return {'message':f"Admin with id {id} updated succesfully"}


@router.post('/admin', response_model=schemas.Admin, tags=['admins'])
def create_staff(request:schemas.Admin, db: Session = Depends(get_db)):
    admin = models.Admin(**request.dict())
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@router.delete('/admin/{id}',tags=['admins'])
def destroy(id, db: Session=Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id==id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Admin with the id {id} not found")
    admin.delete(synchronize_session=False)
    db.commit()
    return 'done'