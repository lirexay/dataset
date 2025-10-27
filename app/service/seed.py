# service/seed.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.user_role import UserRole
from app.entities.user import User
from app.entities.state import State
from app.entities.file import File
from app.entities.dataset import Dataset
from app.entities.request import Request
from app.entities.sell_request import SellRequest
from sqlalchemy import text

from app.core.auth import get_password_hash
# data/seed_data.py

PERSIAN_USER_ROLES = [
    {"title": "مدیر سیستم"},
    {"title": "کارشناس فروش"},
    {"title": "تحلیلگر داده"},
    {"title": "مشتری"},
]

PERSIAN_STATES = [
    {"name": "در انتظار بررسی"},
    {"name": "در حال پردازش"},
    {"name": "تکمیل شده"},
    {"name": "لغو شده"},
]

PERSIAN_USERS = [
    {
        "user_role_id": 1,
        "fname": "علی",
        "lname": "رضایی",
        "username": "admin",
        "password": "admin",  # ⚠️ In real seed, hash it!
        "phone": "09123456789"
    },
    {
        "user_role_id": 2,
        "fname": "سارا",
        "lname": "احمدی",
        "username": "sara_sales",
        "password": "hashed_password_2",
        "phone": "09356789012"
    },
    {
        "user_role_id": 3,
        "fname": "محمد",
        "lname": "حسینی",
        "username": "mohammad_analyst",
        "password": "hashed_password_3",
        "phone": "09101112233"
    },
]

PERSIAN_FILES = [
    {"name": "داده_فروش_ماهانه.xlsx"},
    {"name": "گزارش_تحلیل_مشتریان.csv"},
    {"name": "لیست_محصولات.json"},
]

PERSIAN_DATASETS = [
    {
        "name": "داده‌های فروش سال ۱۴۰۳",
        "description": "مجموع داده‌های فروش شرکت در سال جاری",
        "file_id": 1
    },
    {
        "name": "پایگاه داده مشتریان",
        "description": "اطلاعات کامل مشتریان فعال و غیرفعال",
        "file_id": 2
    }
]

PERSIAN_REQUESTS = [
    {
        "title": "درخواست تحلیل داده فروش",
        "description": "نیاز به گزارش تفصیلی فروش ماهانه با تفکیک محصول",
        "comment": "فوری - برای جلسه هیئت مدیره",
        "state_id": 1,
        "user_requestor_id": 2
    }
]

PERSIAN_SELL_REQUESTS = [
    {
        "title": "درخواست فروش مجموعه داده مشتریان",
        "description": "درخواست دسترسی به داده‌های خام مشتریان برای تیم بازاریابی",
        "comment": "با رعایت قوانین حریم خصوصی",
        "state_id": 2,
        "user_requestor_id": 3
    }
]


class SeedService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def seed_all(self):
        # === 1. Clear tables in reverse dependency order ===
        await self.db.execute(SellRequest.__table__.delete())
        await self.db.execute(Request.__table__.delete())
        await self.db.execute(Dataset.__table__.delete())
        await self.db.execute(User.__table__.delete())
        await self.db.execute(File.__table__.delete())
        await self.db.execute(UserRole.__table__.delete())
        await self.db.execute(State.__table__.delete())

        await self.db.execute(text("ALTER SEQUENCE user_roles_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE states_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE files_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE datasets_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE requests_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE sell_requests_id_seq RESTART WITH 1"))

        # === 3. Seed UserRoles ===
        role_data = [
            {"title": "مدیر سیستم"},
            {"title": "کارشناس فروش"},
            {"title": "تحلیلگر داده"},
        ]
        roles = [UserRole(**r) for r in role_data]
        self.db.add_all(roles)
        await self.db.flush()  # Now roles have real IDs

        # Map role titles to actual objects for reference
        role_map = {r.title: r for r in roles}

        # === 4. Seed States ===
        state_data = [
            {"name": "در انتظار بررسی"},
            {"name": "در حال پردازش"},
            {"name": "تکمیل شده"},
        ]
        states = [State(**s) for s in state_data]
        self.db.add_all(states)
        await self.db.flush()
        state_map = {s.name: s for s in states}

        # === 5. Seed Files ===
        file_data = [
            {"name": "داده_فروش_ماهانه.xlsx"},
            {"name": "گزارش_تحلیل_مشتریان.csv"},
        ]
        files = [File(**f) for f in file_data]
        self.db.add_all(files)
        await self.db.flush()
        file_map = {f.name: f for f in files}

        # === 6. Seed Users (using real role objects) ===
        print(get_password_hash("admin"))
        user_data = [
            {"user_role": role_map["مدیر سیستم"], "fname": "علی", "lname": "رضایی",
                "username": "admin", "password": get_password_hash("admin"), "phone": "09123456789"},
            {"user_role": role_map["کارشناس فروش"], "fname": "سارا", "lname": "احمدی",
                "username": "sara_sales", "password": get_password_hash("pass123"), "phone": "09356789012"},
        ]
        # Convert to User objects with real relationships
        users = []
        for u in user_data:
            role = u.pop("user_role")
            user = User(user_role_id=role.id, **u)
            users.append(user)
        self.db.add_all(users)
        await self.db.flush()
        user_map = {u.username: u for u in users}

        # === 7. Seed Datasets ===
        dataset_data = [
            {"name": "داده‌های فروش سال ۱۴۰۳", "description": "مجموع داده‌های فروش شرکت در سال جاری",
                "file_id": file_map["داده_فروش_ماهانه.xlsx"].id},
        ]
        datasets = [Dataset(**d) for d in dataset_data]
        self.db.add_all(datasets)
        await self.db.flush()

        # === 8. Seed Requests ===
        request_data = [
            {
                "title": "درخواست تحلیل داده فروش",
                "description": "نیاز به گزارش تفصیلی فروش ماهانه با تفکیک محصول",
                "comment": "فوری - برای جلسه هیئت مدیره",
                "state_id": state_map["در انتظار بررسی"].id,
                "user_requestor_id": user_map["sara_sales"].id,
            }
        ]
        requests = [Request(**r) for r in request_data]
        self.db.add_all(requests)
        await self.db.flush()

        # === 9. Seed SellRequests ===
        sell_request_data = [
            {
                "title": "درخواست فروش مجموعه داده مشتریان",
                "description": "درخواست دسترسی به داده‌های خام مشتریان برای تیم بازاریابی",
                "comment": "با رعایت قوانین حریم خصوصی",
                "state_id": state_map["در حال پردازش"].id,
                "user_requestor_id": user_map["admin"].id,
            }
        ]
        sell_requests = [SellRequest(**sr) for sr in sell_request_data]
        self.db.add_all(sell_requests)

        await self.db.commit()
        return {"status": "success", "message": "داده‌های نمونه فارسی با موفقیت بارگذاری شدند."}
