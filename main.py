import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from fastapi import FastAPI
from api.users import router as users_router
from api.bots import router as bots_router
from api.dashboard import router as dashboard_router

app = FastAPI()

app.include_router(dashboard_router)
app.include_router(users_router)
app.include_router(bots_router)

@app.get("/")
def root():
    return {"status": "ok"}
