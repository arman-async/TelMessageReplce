import uvicorn
from fastapi import Depends, FastAPI
from sqladmin import Admin

from app import db

from . import auth

# ===== FastAPI =====
app = FastAPI(
    title="Telgram Bot", version="1.0.0", dependencies=[Depends(auth.QureyToken)]
)

# ===== SQLAdmin =====
authentication_backend = auth.Dashboard(
    secret_key="secret",
)

dashboard = Admin(
    app=app,
    engine=db.engine,
    title="Dashboard",
    templates_dir="templates",
    base_url="/dashboard",
    authentication_backend=authentication_backend,
)

# ===== Imports =====
from . import view
from . import router
# ===== Views =====
dashboard.add_view(view.ForcedSubscription)
dashboard.add_view(view.MessageAction)

# ==== Includ Routes =====
app.include_router(router.forced_subscription)
app.include_router(router.message_action)

# ===== Run =====
async def run():
    config_uvicorn = uvicorn.Config(app, host="0.0.0.0", port=9000, log_level="info")
    server = uvicorn.Server(config_uvicorn)
    await server.serve()
