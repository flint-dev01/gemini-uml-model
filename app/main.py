from fastapi import FastAPI
from app.routes import uml_routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}

app.include_router(uml_routes.router, prefix="/uml")

