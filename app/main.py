#!/usr/bin/python3
import os

from fastapi import FastAPI
from .routers.things import points, polygons, animals, machines
from .routers.measurements import devices, sensors, samples
from .routers import attachments
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from app import __version__

load_dotenv()
DB_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
DB_PASS = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
DB_URL = f"mongodb://{DB_USER}:{DB_PASS}@localhost"

app = FastAPI(title="{ farm-twin }", version=__version__)

app.include_router(sensors.router, prefix='/measurements')
app.include_router(devices.router, prefix='/measurements')
app.include_router(samples.router, prefix='/measurements')

app.include_router(points.router, prefix='/things')
app.include_router(polygons.router, prefix='/things')
app.include_router(animals.router, prefix='/things')
app.include_router(machines.router, prefix='/things')

app.include_router(attachments.router)


async def open_db() -> AsyncIOMotorClient:
    app.state.mongodb = AsyncIOMotorClient(DB_URL)

    _ft = app.state.mongodb['farm-twin']

    app.state.devices = _ft['measurements']['devices']
    app.state.sensors = _ft['measurements']['sensors']
    app.state.samples = _ft['measurements']['samples']

    app.state.points = _ft['things']['points']
    app.state.polygons = _ft['things']['polygons']
    app.state.animals = _ft['things']['animals']
    app.state.animals = _ft['things']['machines']

    app.state.attachments = _ft['attachments']


async def create_indexes():
    app.state.devices.create_index(["tag", "vendor"], unique=True)
    app.state.points.create_index({"point": "2dsphere"}, unique=True)
    app.state.polygons.create_index(["polygon"], unique=True)
    app.state.sensors.create_index(["device", "measurement"], unique=True)
    _attachment_index = ["device", "thing", "start"]
    app.state.attachments.create_index(_attachment_index, unique=True)
    _sample_index = ["device", "sensor", "timestamp", "predicted"]
    app.state.samples.create_index(_sample_index, unique=True)


async def close_db():
    app.state.mongodb.close()

app.add_event_handler('startup', open_db)
app.add_event_handler('startup', create_indexes)
app.add_event_handler('shutdown', close_db)


@app.get("/version/", response_description="API Version")
async def version():
    return {"version": __version__}
