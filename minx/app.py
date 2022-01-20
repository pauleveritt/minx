import asyncio

from fastapi import FastAPI
from watchgod import awatch

WATCH_DIR = "docs"
app = FastAPI()


async def watch_changes():
    print(f"Watching changes in directory: {WATCH_DIR}")
    async for changes in awatch(WATCH_DIR):
        print(changes)


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(watch_changes())


@app.on_event("shutdown")
async def shutdown_event():
    print("On shutdown")


@app.get("/")
def read_root():
    return {"Hello": "World"}
