from sqlalchemy.orm import Session

import model


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.ProjectTable).offset(skip).limit(limit).all()


def get_project(db: Session, user_id: int):
    return db.query(model.ProjectTable).filter(model.ProjectTable.id == user_id).first()


def del_project(db: Session, project_id: int):
    return db.query(model.ProjectTable).filter(model.ProjectTable.id == project_id).first()
