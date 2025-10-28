# service/seed.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.entities.dataset_category import DatasetCategory
from app.entities.user_role import UserRole
from app.entities.user import User
from app.entities.state import State
from app.entities.file import File
from app.entities.dataset import Dataset
from app.entities.request import Request
from app.entities.sell_request import SellRequest
from app.core.auth import get_password_hash

# Use your actual seed data (defined above or imported)
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

PERSIAN_FILES = [
    {"name": "داده_فروش_ماهانه.xlsx"},
    {"name": "گزارش_تحلیل_مشتریان.csv"},
    {"name": "لیست_محصولات.json"},
]

PERSIAN_DATASET_CATEGORIES = [
    {"name": "فروش"},
    {"name": "بازاریابی"},
    {"name": "منابع انسانی"},
    {"name": "مالی"},
]

PERSIAN_USERS = [
    {
        "user_role_title": "مدیر سیستم",
        "fname": "علی",
        "lname": "رضایی",
        "username": "admin",
        "password": "admin",
        "phone": "09123456789"
    },
    {
        "user_role_title": "کارشناس فروش",
        "fname": "سارا",
        "lname": "احمدی",
        "username": "sara_sales",
        "password": "pass123",
        "phone": "09356789012"
    },
]

PERSIAN_DATASETS = [
    {
        "name": "داده‌های فروش سال ۱۴۰۳",
        "description": "مجموع داده‌های فروش شرکت در سال جاری",
        "file_name": "داده_فروش_ماهانه.xlsx",
        "category_name": "فروش"
    },
    {
        "name": "پایگاه داده مشتریان",
        "description": "اطلاعات کامل مشتریان فعال و غیرفعال",
        "file_name": "گزارش_تحلیل_مشتریان.csv",
        "category_name": "بازاریابی"
    }
]

PERSIAN_REQUESTS = [
    {
        "title": "درخواست تحلیل داده فروش",
        "description": "نیاز به گزارش تفصیلی فروش ماهانه با تفکیک محصول",
        "comment": "فوری - برای جلسه هیئت مدیره",
        "state_name": "در انتظار بررسی",
        "username": "sara_sales"
    }
]

PERSIAN_SELL_REQUESTS = [
    {
        "title": "درخواست فروش مجموعه داده مشتریان",
        "description": "درخواست دسترسی به داده‌های خام مشتریان برای تیم بازاریابی",
        "comment": "با رعایت قوانین حریم خصوصی",
        "state_name": "در حال پردازش",
        "username": "admin"
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
        await self.db.execute(DatasetCategory.__table__.delete())  # ← NEW
        await self.db.execute(User.__table__.delete())
        await self.db.execute(File.__table__.delete())
        await self.db.execute(UserRole.__table__.delete())
        await self.db.execute(State.__table__.delete())

        # === 2. Reset sequences (PostgreSQL) ===
        await self.db.execute(text("ALTER SEQUENCE user_roles_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE states_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE files_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        # ← NEW
        await self.db.execute(text("ALTER SEQUENCE dataset_categories_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE datasets_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE requests_id_seq RESTART WITH 1"))
        await self.db.execute(text("ALTER SEQUENCE sell_requests_id_seq RESTART WITH 1"))

        # === 3. Seed UserRoles ===
        roles = [UserRole(**r) for r in PERSIAN_USER_ROLES]
        self.db.add_all(roles)
        await self.db.flush()
        role_map = {r.title: r for r in roles}

        # === 4. Seed States ===
        states = [State(**s) for s in PERSIAN_STATES]
        self.db.add_all(states)
        await self.db.flush()
        state_map = {s.name: s for s in states}

        # === 5. Seed Files ===
        files = [File(**f) for f in PERSIAN_FILES]
        self.db.add_all(files)
        await self.db.flush()
        file_map = {f.name: f for f in files}

        # === 6. Seed Categories ===
        categories = [DatasetCategory(**c) for c in PERSIAN_DATASET_CATEGORIES]
        self.db.add_all(categories)
        await self.db.flush()
        category_map = {c.name: c for c in categories}

        # === 7. Seed Users ===
        users = []
        for u in PERSIAN_USERS:
            role = role_map[u["user_role_title"]]
            user = User(
                user_role_id=role.id,
                fname=u["fname"],
                lname=u["lname"],
                username=u["username"],
                password=get_password_hash(u["password"]),
                phone=u["phone"]
            )
            users.append(user)
        self.db.add_all(users)
        await self.db.flush()
        user_map = {u.username: u for u in users}

        # === 8. Seed Datasets ===
        datasets = []
        for d in PERSIAN_DATASETS:
            dataset = Dataset(
                name=d["name"],
                description=d["description"],
                file_id=file_map[d["file_name"]].id,
                category_id=category_map[d["category_name"]].id
            )
            datasets.append(dataset)
        self.db.add_all(datasets)
        await self.db.flush()

        # === 9. Seed Requests ===
        requests = []
        for r in PERSIAN_REQUESTS:
            req = Request(
                title=r["title"],
                description=r["description"],
                comment=r["comment"],
                state_id=state_map[r["state_name"]].id,
                user_requestor_id=user_map[r["username"]].id
            )
            requests.append(req)
        self.db.add_all(requests)
        await self.db.flush()

        # === 10. Seed SellRequests ===
        sell_requests = []
        for sr in PERSIAN_SELL_REQUESTS:
            sell_req = SellRequest(
                title=sr["title"],
                description=sr["description"],
                comment=sr["comment"],
                state_id=state_map[sr["state_name"]].id,
                user_requestor_id=user_map[sr["username"]].id
            )
            sell_requests.append(sell_req)
        self.db.add_all(sell_requests)

        await self.db.commit()
        return {"status": "success", "message": "داده‌های نمونه فارسی با موفقیت بارگذاری شدند."}
