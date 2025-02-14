from fastapi import FastAPI
import uvicorn
from routing.devices import router as router_devices
from routing.users import router as router_users
from routing.analitic_control import router as router_analitic_control
from fastapi.middleware.cors import CORSMiddleware
from middlewares.log_middleware import log_requests

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    # "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)


@app.get("/home",tags=['Для примера'])
def get_home():
    return "Hello my owner!"

app.include_router(router_devices)
app.include_router(router_users)
app.include_router(router_analitic_control)






if __name__=="__main__":
    uvicorn.run("main:app",reload=True) 