#!/usr/bin/python3
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app import __version__

from .routers import attachments
from .routers.events import attention, withdrawal
from .routers.events.feeding import feed_intake
from .routers.events.milking import (drying_off, lactation_status,
                                     test_day_result, visit)
from .routers.events.movement import arrival, birth, death, departure
from .routers.events.observations import carcass, health_status, position
from .routers.events.performance import conformation, group_weight, weight
from .routers.events.reproduction import (repro_abortion, repro_do_not_breed,
                                          repro_heat, repro_insemination,
                                          repro_mating_recommendation,
                                          repro_parturition,
                                          repro_pregnancy_check, repro_status)
from .routers.measurements import devices, samples, sensors
from .routers.objects import (animals, embryo, feed, feed_storage, machines,
                              medicine, points, polygons, ration, semen_straw)

load_dotenv()
DB_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
DB_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
DB_URL = f"mongodb://{DB_USER}:{DB_PASS}@localhost"

app = FastAPI(title="{ farm-twin }", version=__version__)

app.include_router(sensors.router, prefix="/measurements")
app.include_router(devices.router, prefix="/measurements")
app.include_router(samples.router, prefix="/measurements")

app.include_router(points.router, prefix="/objects")
app.include_router(polygons.router, prefix="/objects")
app.include_router(animals.router, prefix="/objects")
app.include_router(machines.router, prefix="/objects")
app.include_router(feed.router, prefix="/objects")
app.include_router(feed_storage.router, prefix="/objects")
app.include_router(medicine.router, prefix="/objects")
app.include_router(ration.router, prefix="/objects")
app.include_router(embryo.router, prefix="/objects")
app.include_router(semen_straw.router, prefix="/objects")

app.include_router(feed_intake.router, prefix="/events/feeding")

app.include_router(attention.router, prefix="/events")
app.include_router(withdrawal.router, prefix="/events")

app.include_router(conformation.router, prefix="/events/performance")
app.include_router(weight.router, prefix="/events/performance")
app.include_router(group_weight.router, prefix="/events/performance")


app.include_router(drying_off.router, prefix="/events/milking")
app.include_router(visit.router, prefix="/events/milking")
app.include_router(lactation_status.router, prefix="/events/milking")
app.include_router(test_day_result.router, prefix="/events/milking")

app.include_router(arrival.router, prefix="/events/movement")
app.include_router(birth.router, prefix="/events/movement")
app.include_router(death.router, prefix="/events/movement")
app.include_router(departure.router, prefix="/events/movement")

app.include_router(carcass.router, prefix="/events/observations")
app.include_router(health_status.router, prefix="/events/observations")
app.include_router(position.router, prefix="/events/observations")

app.include_router(repro_status.router, prefix="/events/reproduction")
app.include_router(repro_abortion.router, prefix="/events/reproduction")
app.include_router(repro_do_not_breed.router, prefix="/events/reproduction")
app.include_router(repro_heat.router, prefix="/events/reproduction")
app.include_router(repro_insemination.router, prefix="/events/reproduction")
app.include_router(repro_mating_recommendation.router,
                   prefix="/events/reproduction")
app.include_router(repro_parturition.router, prefix="/events/reproduction")
app.include_router(repro_pregnancy_check.router, prefix="/events/reproduction")

app.include_router(attachments.router)


async def open_db() -> AsyncIOMotorClient:
    app.state.mongodb = AsyncIOMotorClient(DB_URL)

    _ft = app.state.mongodb["farm-twin"]

    app.state.devices = _ft["measurements"]["devices"]
    app.state.sensors = _ft["measurements"]["sensors"]
    app.state.samples = _ft["measurements"]["samples"]

    app.state.points = _ft["objects"]["points"]
    app.state.polygons = _ft["objects"]["polygons"]
    app.state.animals = _ft["objects"]["animals"]
    app.state.machines = _ft["objects"]["machines"]
    app.state.feed = _ft["objects"]["feed"]
    app.state.feed_storage = _ft["objects"]["feed_storage"]
    app.state.medicine = _ft["objects"]["medicine"]
    app.state.ration = _ft["objects"]["ration"]
    app.state.embryo = _ft["objects"]["embryo"]
    app.state.semen_straw = _ft["objects"]["semen_straw"]

    app.state.attention = _ft["events"]["attention"]
    app.state.withdrawal = _ft["events"]["withdrawal"]

    app.state.feed_intake = _ft["events"]["feeding"]["feed_intake"]

    app.state.conformation = _ft["events"]["performance"]["conformation"]
    app.state.weight = _ft["events"]["performance"]["weight"]
    app.state.group_weight = _ft["events"]["performance"]["group_weight"]

    app.state.drying_off = _ft["events"]["milking"]["drying_off"]
    app.state.visit = _ft["events"]["milking"]["visit"]
    app.state.lactation_status = _ft["events"]["milking"]["lactation_status"]
    app.state.test_day_result = _ft["events"]["milking"]["test_day_result"]

    app.state.arrival = _ft["events"]["movement"]["arrival"]
    app.state.birth = _ft["events"]["movement"]["birth"]
    app.state.death = _ft["events"]["movement"]["death"]
    app.state.departure = _ft["events"]["movement"]["departure"]

    app.state.carcass = _ft["events"]["observations"]["carcass"]
    app.state.health_status = _ft["events"]["observations"]["health_status"]
    app.state.position = _ft["events"]["observations"]["position"]

    app.state.repro_status = _ft["events"]["reproduction"]["repro_status"]
    app.state.repro_abortion = _ft["events"]["reproduction"]["repro_abortion"]
    app.state.repro_do_not_breed = _ft["events"]["reproduction"]["repro_do_not_breed"]
    app.state.repro_heat = _ft["events"]["reproduction"]["repro_heat"]
    app.state.repro_insemination = _ft["events"]["reproduction"]["repro_insemination"]
    app.state.repro_mating_recommendation = _ft["events"]["reproduction"][
        "repro_mating_recommendation"
    ]
    app.state.repro_parturition = _ft["events"]["reproduction"]["repro_parturition"]
    app.state.repro_pregnancy_check = _ft["events"]["reproduction"][
        "repro_pregnancy_check"
    ]

    app.state.attachments = _ft["attachments"]


async def create_indexes():
    app.state.devices.create_index(["serial", "manufacturer"], unique=True)
    app.state.points.create_index({"point": "2dsphere"}, unique=True)
    app.state.polygons.create_index(["polygon"], unique=True)
    app.state.sensors.create_index(
        ["device", "serial", "measurement"], unique=True)
    _attachment_index = ["device", "thing", "start"]
    app.state.attachments.create_index(_attachment_index, unique=True)
    _sample_index = ["device", "sensor", "timestamp", "predicted"]
    app.state.samples.create_index(_sample_index, unique=True)


async def close_db():
    app.state.mongodb.close()


app.add_event_handler("startup", open_db)
app.add_event_handler("startup", create_indexes)
app.add_event_handler("shutdown", close_db)


@app.get("/version/", response_description="API Version")
async def version():
    return {"version": __version__}
