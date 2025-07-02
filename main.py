#main.py
from fastapi import FastAPI
from database import engine
import models  # meng-import agar tabel terdaftar
from routers import signup_router, mining_router, balance_router, export_router, referral_router
from routers import export

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# register routers
app.include_router(signup_router)
app.include_router(mining_router)
app.include_router(balance_router)
app.include_router(export_router)
app.include_router(referral_router)
