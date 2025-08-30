from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

import datetime
from repository.user import *
from util.util import *
from util import util
from model import database, model

router = APIRouter(tags=["seed"], prefix="/seed")


@router.get("/seed/")
async def add_proposal(db: Session = Depends(get_db)):

    db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    result = db.execute(text("SHOW TABLES;"))
    tables = [row[0] for row in result.fetchall()]
    for table in tables:
        db.execute(text(f"DROP TABLE IF EXISTS {table};"))

    model.Base.metadata.create_all(database.engine)

    new_user_roules = [
        UserRole(title="ادمین"),  # 1
        UserRole(title="شخصیت حقوقی"),  # 2
        UserRole(title="کاربر عادی"),  # 3
    ]
    db.add_all(new_user_roules)
    db.commit()

    roles = db.query(UserRole).all()
    new_file = File(name="file.pdf")
    db.add(new_file)
    db.commit()
    file_id = db.query(File).first().id

    new_users = [
        User(
            user_role_id=roles[0].id,
            fname="جواد",
            lname="جوادی",
            username="admin",
            password=util.hash(
                "admin"
            ),  # فرض می‌کنیم util.hash یک تابع برای رمزنگاری است
            phone="09181020300",
        ),
        User(
            user_role_id=roles[1].id,
            fname="علی",
            lname="اکبری",
            username="admin2",
            password=util.hash("admin"),
            phone="09182020301",
        ),
        User(
            user_role_id=roles[2].id,
            fname="سارا",
            lname="موسوی",
            username="admin3",
            password=util.hash("admin"),
            phone="09183020302",
        ),
    ]
    db.add_all(new_users)
    db.commit()

    states = [
        State(name="در حال بررسی"),
        State(name="تأیید شده"),
        State(name="رد شده"),
    ]
    db.add_all(states)
    db.commit()

    existing_states = db.query(State).all()
    users = db.query(User).all()
    requests = [
        Request(
            title="درخواست پروژه IT",
            description="نیاز به توسعه نرم‌افزار برای سیستم مدیریت",
            comment="لطفا با جزئیات بیشتر تماس بگیرید.",
            state_id=existing_states[0].id,
            user_requestor_id=users[0].id,
        ),
        Request(
            title="پروژه تحقیقاتی",
            description="تحقیق در زمینه هوش مصنوعی",
            comment="قابل تایید است",
            state_id=existing_states[1].id,
            user_requestor_id=users[1].id,
        ),
        Request(
            title="بهبود فرآیند کشاورزی",
            description="استفاده از تکنولوژی‌های نوین در کشاورزی",
            comment="قابل تایید نیست.",
            state_id=existing_states[2].id,
            user_requestor_id=users[2].id,
        ),
    ]
    db.add_all(requests)
    db.commit()

    return {"response": "ok"}
