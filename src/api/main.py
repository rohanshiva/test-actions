from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from deta import Deta
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

deta = Deta()

pages = deta.Base("tpages")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Page(BaseModel):
    key: str
    text: str
    locked: bool = False
    updated: str = None
    # months: list = None
    # week: str = None


@app.get("/")
def read_root():
    return {"Hello": "There"}


@app.get("/dates")
def read_root():
    n = datetime.now()
    w = n.isocalendar()[1]
    return {
        "year": {"0": f"y{n.year-1}", "1": f"y{n.year}", "2": f"y{n.year+1}"},
        "month": {
            "0": f"m{n.year}{n.month-1:02d}",
            "1": f"m{n.year}{n.month:02d}",
            "2": f"m{n.year}{n.month+1:02d}",
        },
        "day": {
            "0": f"d{n.year}{n.month:02d}{n.day-1:02d}",
            "1": f"d{n.year}{n.month:02d}{n.day:02d}",
            "2": f"d{n.year}{n.month:02d}{n.day+1:02d}",
        },
        "week": {
            "0": f"w{n.year}{w-1:02d}",
            "1": f"w{n.year}{w:02d}",
            "2": f"w{n.year}{w+1:02d}",
        },
    }


@app.post("/pages")
def create_user(page: Page):
    u = pages.put(page.dict())
    return u


@app.get("/pages/{key}")
def getpage(key:str):
    return pages.get(key) or {}


# @app.get("/users/{uid}")
# def get_user(uid: str):
#     user = users.get(uid)
#     if user:
#         return user
#     return JSONResponse({"message": "user not found"}, status_code=404)


# # @app.patch("/users/{uid}")
# # def update_user(uid: str, uu: UserUpdate):
# #     updates = {k:v for k,v in uu.dict().items() if v is not None}
# #     try:
# #         users.update(updates, uid)
# #         return users.get(uid)
# #     except Exception:
# #         return JSONResponse({"message": "user not found"}, status_code=404)


# @app.delete("/users/{uid}")
# def delete_user(uid: str):
#     users.delete(uid)
#     return
