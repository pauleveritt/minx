from fastapi import FastAPI

from minx.watchers import watcher

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("On startup with", watcher)

    # The watcher instance is an async iterator. It says it works by:
    #  "using a threaded executor"
    # So in theory, the code below should work. But it hangs processing:
    #   - We never get to the print
    #   - The server no longer answers requests
    #   - We don't get to shutdown
    async for changes in watcher.get():
        print(changes)
    print("We never get here")


@app.on_event("shutdown")
async def shutdown_event():
    print("On shutdown")


@app.get("/")
def read_root():
    return {"Hello": "World"}
