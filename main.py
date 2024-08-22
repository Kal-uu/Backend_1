import os

from fastapi import FastAPI, Depends, UploadFile, HTTPException, File, Form
from sqlalchemy.orm import Session

import crud
import model
import schemes
import utils
from database import engine, SessionLocal

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/new_project', response_model=schemes.ProjectResponse, dependencies=[Depends(get_db)])
def create_proj(title: str,
                description: str,
                video: UploadFile = Form(),
                image: UploadFile = File(...),
                db: Session = Depends(get_db)):
    if not image.filename.endswith('.png'):
        raise HTTPException(status_code=400, detail='Image must be .png')
    else:
        image = utils.save_file(image, "image") if image else None

    if not video.filename.endswith('.mp4'):
        raise HTTPException(status_code=400, detail='Video must be .mp4')
    else:
        video = utils.save_file(video, "video") if video else None

    new_proj = model.ProjectTable(title=title, description=description,
                                  image=image, video=video)

    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)
    return new_proj


@app.get("/projects/", response_model=list[schemes.ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db=db, skip=skip, limit=limit)
    return projects


@app.get("/project/{id}", response_model=schemes.ProjectResponse)
def read_project(proj_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(user_id=proj_id, db=db)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    return project


@app.delete("/project/{proj_id}", response_model=schemes.ProjectResponse)
def delete_project(proj_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(user_id=proj_id, db=db)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    elif project:
        os.remove('C:/Users/Dell/DataspellProjects/Backend_3/media/video/' + project.video)
    elif project:
        os.remove('C:/Users/Dell/DataspellProjects/Backend_3/media/image/' + project.image)

    db.delete(project)
    db.commit()

