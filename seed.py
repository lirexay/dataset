from util.util import *
from sqlalchemy.orm import Session
from model.model import *
import datetime
from util import util

db = database.SessionLocal()
db.delete

# new_user_roules = [
#     UserRole(title="کارگزار"),
#     UserRole(title="کاشف"),
#     UserRole(title="کاربر"),
#     UserRole(title="ناظر"),
#     UserRole(title="استاد راهنما"),
# ]
# db.add_all(new_user_roules)
# db.commit()


# file_id = db.query(File).first().id
# rolese = db.query(UserRole).all()
# new_file = File(info="file.pdf", access_id=rolese[0].id)
# db.add(new_file)
# db.commit()

# new_users = [
#     User(
#         user_type_id=rolese[0].id,
#         fname="جواد",
#         lname="جوادی",
#         father_name="محمدجواد",
#         resume_file_id=file_id,
#         birth=datetime.datetime.now(),
#         address="همدان-جوادیه",
#         username="admin",
#         password=util.hash("admin"),
#         phone="09181020300",
#         active=True,
#     ),
#     User(
#         user_type_id=rolese[1].id,
#         fname="علی",
#         lname="اکبری",
#         father_name="حسن",
#         birth=datetime.datetime.now(),
#         resume_file_id=file_id,
#         address="تهران-اکبرآباد",
#         username="admin2",
#         password=util.hash("admin"),
#         phone="09182020301",
#         active=True,
#     ),
#     User(
#         user_type_id=rolese[2].id,
#         fname="سارا",
#         lname="موسوی",
#         father_name="محمد",
#         birth=datetime.datetime.now(),
#         resume_file_id=file_id,
#         address="اصفهان-موسوی",
#         username="admin3",
#         password=util.hash("admin"),
#         phone="09183020302",
#         active=True,
#     ),
#     User(
#         user_type_id=rolese[3].id,
#         fname="زهرا",
#         lname="حسینی",
#         father_name="علی",
#         birth=datetime.datetime.now(),
#         resume_file_id=file_id,
#         address="شیراز-حسینیه",
#         username="admin4",
#         password=util.hash("admin"),
#         phone="09184020303",
#         active=True,
#     ),
#     User(
#         user_type_id=rolese[4].id,
#         fname="رضا",
#         lname="نیکو",
#         father_name="سید",
#         birth=datetime.datetime.now(),
#         resume_file_id=file_id,
#         address="مشهد-رضوی",
#         username="admin5",
#         password=util.hash("admin"),
#         phone="09185020304",
#         active=True,
#     ),
# ]
# db.add_all(new_users)
# db.commit()

# new_RFP_fields = [
#     RFPField(title="صنعت خودرو"),
#     RFPField(title="کامپیوتر و it"),
#     RFPField(title="کشاورزی"),
#     RFPField(title="صنایع شیمی"),
#     RFPField(title="صنایع هوافضا"),
#     RFPField(title="امنیت سایبری"),
#     RFPField(title="هوش مصنوعی"),
#     RFPField(title="علوم انسانی"),
# ]
# db.add_all(new_RFP_fields)
# db.commit()

# fieldss = db.query(RFPField).all()

# new_rfps = [
#     RFP(
#         info="درخواست پروژه IT و نرم‌افزار", file_id=file_id, RFP_field_id=fieldss[1].id
#     ),
#     RFP(info="طرح برای بهبود کشاورزی", file_id=file_id, RFP_field_id=fieldss[2].id),
#     RFP(info="نیاز به تأمین مواد شیمیایی", file_id=file_id, RFP_field_id=fieldss[3].id),
#     RFP(
#         info="پروژه تحقیقاتی در صنعت هوافضا",
#         file_id=file_id,
#         RFP_field_id=fieldss[4].id,
#     ),
#     RFP(info="ایجاد زیرساخت امنیت سایبری", file_id=file_id, RFP_field_id=fieldss[5].id),
#     RFP(
#         info="تحقیق و توسعه در هوش مصنوعی", file_id=file_id, RFP_field_id=fieldss[6].id
#     ),
#     RFP(info="پروژه در علوم انسانی", file_id=file_id, RFP_field_id=fieldss[7].id),
#     RFP(
#         info="برنامه‌ریزی برای توسعه صنعت خودرو",
#         file_id=file_id,
#         RFP_field_id=fieldss[7].id,
#     ),
#     RFP(info="توسعه نرم‌افزارهای IT", file_id=file_id, RFP_field_id=fieldss[1].id),
#     RFP(info="بهینه‌سازی در کشاورزی", file_id=file_id, RFP_field_id=fieldss[2].id),
#     RFP(
#         info="تحقیقات در زمینه صنایع شیمیایی",
#         file_id=file_id,
#         RFP_field_id=fieldss[3].id,
#     ),
#     RFP(info="نوآوری در صنعت هوافضا", file_id=file_id, RFP_field_id=fieldss[4].id),
#     RFP(info="تقویت امنیت سایبری", file_id=file_id, RFP_field_id=fieldss[5].id),
#     RFP(info="ایجاد پروژه‌های هوش مصنوعی", file_id=file_id, RFP_field_id=fieldss[6].id),
# ]
# db.add_all(new_rfps)
# db.commit()

# user_id = db.query(User).first().id
# RFP_id = db.query(RFP).first().id
# new_proposal = [
#     Proposal(
#         info="پروپوزال۱ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۲ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         file_id=file_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۳ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         file_id=file_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۴ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         file_id=file_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۵ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۶ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۷ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۸ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۹ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۱۰ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۱۱ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۱۲ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
#     Proposal(
#         info="پروپوزال۱۳ ",
#         RFP_id=RFP_id,
#         user_id=user_id,
#         state=1,
#         comment="",
#     ),
# ]
# db.add_all(new_proposal)
# db.commit()

# proposals = db.query(Proposal).all()

# users_for_roles = [
#     db.query(User).filter(User.user_type_id == rolese[0].id).first(),
#     db.query(User).filter(User.user_type_id == rolese[1].id).first(),
#     db.query(User).filter(User.user_type_id == rolese[2].id).first(),
#     db.query(User).filter(User.user_type_id == rolese[3].id).first(),
#     db.query(User).filter(User.user_type_id == rolese[4].id).first(),
# ]


# new_projects = [
#     Project(
#         title="project 1",
#         proposal_id=proposals[0].id,
#         user_supervisor_id=users_for_roles[3].id,
#         user_discoverer_id=users_for_roles[1].id,
#         user_master_id=users_for_roles[4].id,
#         user_broker_id=users_for_roles[0].id,
#         user_user_id=users_for_roles[2].id,
#     ),
#     Project(
#         title="project 2",
#         proposal_id=proposals[1].id,
#         user_supervisor_id=users_for_roles[3].id,
#         user_discoverer_id=users_for_roles[1].id,
#         user_master_id=users_for_roles[4].id,
#         user_broker_id=users_for_roles[0].id,
#         user_user_id=users_for_roles[2].id,
#     ),
#     Project(
#         title="project 3",
#         proposal_id=proposals[2].id,
#         user_supervisor_id=users_for_roles[3].id,
#         user_discoverer_id=users_for_roles[1].id,
#         user_master_id=users_for_roles[4].id,
#         user_broker_id=users_for_roles[0].id,
#         user_user_id=users_for_roles[2].id,
#     ),
# ]


# db.add_all(new_projects)
# db.commit()
# project_id = db.query(Project).first().id
# new_reports = [
#     Report(
#         info="report 1",
#         project_id=project_id,
#         comment="none",
#         state=project_id,
#     ),
#     Report(
#         info="report 2",
#         project_id=project_id,
#         comment="none",
#         state=2,
#     ),
#     Report(
#         info="report 2",
#         project_id=project_id,
#         comment="none",
#         state=3,
#     ),
# ]
# db.add_all(new_reports)
# db.commit()

# report_id = db.query(Report).first().id
# new_report_files = [
#     ReportFile(
#         info="file 1",
#         report_id=report_id,
#         file_id=file_id,
#     ),
#     ReportFile(
#         info="file 2",
#         report_id=report_id,
#         file_id=file_id,
#     ),
# ]
# db.add_all(new_report_files)
# db.commit()
