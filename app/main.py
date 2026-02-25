"""
This is the main entry point of the FastAPI application. It initializes the app, includes all the necessary routes, 
and sets up any required middleware or event handlers. The app is structured to be modular, with separate files for 
models, schemas, routes, and database interactions. This file will import the routes from the app.routes package and 
include them in the FastAPI app instance. It also serves as the central place to configure any global settings or dependencies 
that the app might need. 
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import user, instructor, yoga_class, yoga_session, yoga_schedule, booking
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database tables
    await init_db()
    yield
    # Shutdown: Add cleanup code here if needed

app = FastAPI(title="Fitness Club API", version="1.0.0", lifespan=lifespan)

app.include_router(user.router)
app.include_router(instructor.router)
app.include_router(yoga_class.router)
app.include_router(yoga_session.router)
app.include_router(yoga_schedule.router)
app.include_router(booking.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fitness Club API!"}