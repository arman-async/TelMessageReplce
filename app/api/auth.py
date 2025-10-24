from fastapi import HTTPException, Query, Request
from sqladmin.authentication import AuthenticationBackend

from app import config

USER = config.Dashboard().USER
PASSWORD = config.Dashboard().PASSWORD
TOKEN = config.API().TOKEN

class Dashboard(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not USER == username:
            return False
        if not PASSWORD == password:
            return False

        request.session.update({"token": f"{USER}:{PASSWORD}"})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        if token.split(":")[0] != USER:
            return False
        if token.split(":")[1] != PASSWORD:
            return False

        return True


async def QureyToken(token: str = Query(..., alias="api_token")):
    if token != TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API token")
