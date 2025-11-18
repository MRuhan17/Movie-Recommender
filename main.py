from fastapi import FastAPI
from main import router   # adjust this import

app = FastAPI()
app.include_router(router)
