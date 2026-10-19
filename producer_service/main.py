from contextlib import asynccontextmanager
from fastapi import FastAPI
from producer.routers.author_router import router as author_router
from producer.kafka_client import close_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_producer()


app = FastAPI(
    title="Author Post Service",
    description="API designed to post authors",
    version="1.0",
    lifespan=lifespan,
)

app.include_router(author_router)