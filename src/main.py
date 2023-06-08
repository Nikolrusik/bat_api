from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from auth.router import router as auth_router
from shop.router import router as product_router


app = FastAPI(
    title="BAT agregator",
    prefix='/api'
)


@app.on_event("startup")
async def startap_event():
    redis = aioredis.from_url(
        'redis://127.0.0.1', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

app.include_router(auth_router)
app.include_router(product_router)


@app.get("/")
async def root():
    return {'message': 'Hello World'}
