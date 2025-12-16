from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from api import solve, states
from db.base import init_db

import uvicorn

app = FastAPI(title="Rubik's Solver API")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including all the routers
app.include_router(states.router)
app.include_router(solve.router)

@app.get("/")
def root():
    return {"message": "Rubik's Cube Solver Backend Running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
