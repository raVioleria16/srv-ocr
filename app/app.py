from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routers import endpoints

from service import service as srv

@asynccontextmanager
async def lifespan(app: FastAPI):
    await srv.register_service(provider=srv.config.ext_srv.srv_configuration_manager.provider,
                               configuration=srv.config.model_dump(exclude="ext_srv"))
    await srv.initialize_service()
    yield


app = FastAPI(
    title=f"FastAPI Application",
    description="This is a simple FastAPI application with a few endpoints.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/endpoints",  # Set the URL for the Swagger UI
)

# Include the endpoints from the routers file
app.include_router(endpoints.router, tags=["Endpoints"])