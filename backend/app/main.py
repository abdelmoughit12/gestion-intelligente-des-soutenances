from fastapi import FastAPI
from app.api import user

app = FastAPI(title="My Backend")

routers = [
    (user.router, "/users", ["Users"]),
]

for router, prefix, tags in routers:
    app.include_router(router, prefix=prefix, tags=tags)
