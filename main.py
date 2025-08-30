from fastapi import FastAPI
import routers
from model import database, model
import ssl
from routers import (
    authentication,
    dataset,
    requests,
    # user,
    file,
    seed,
)
from fastapi.middleware.cors import CORSMiddleware

# from seed import seeding

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("./cert.pem", keyfile="./key.pem")


model.Base.metadata.create_all(database.engine)
app.include_router(authentication.router)
app.include_router(seed.router)
app.include_router(dataset.router)
# app.include_router(user.router)
app.include_router(requests.router)
app.include_router(file.router)
app.include_router(seed.router)
# seeding()
