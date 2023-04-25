from fastapi import FastAPI
from auth.router import router as auth_router


app = FastAPI(
    title = "BAT agregator"
)

app.include_router(auth_router)

 
@app.get("/")
async def root():
    return {'message': 'Hello World'}


async def products():
    pass 
    # get product list

async def user():
    pass
    # get user info