from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import router as education_router
import logging
from backend.client import engine

def create_app() -> FastAPI:
    """
    Application factory function that returns a FastAPI instance.
    This is a common pattern for creating a FastAPI application.
    """
    app = FastAPI(title='Education Intelligence API',
                  description='API for managing an educational platform',
                  version='1.0.0')

    app.include_router(education_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Specify domains as needed
        allow_credentials=True,
        allow_methods=["*"],  # Or specify methods ['GET', 'POST', etc.]
        allow_headers=["*"]
    )

    # Event handlers for startup and shutdown
    @app.on_event("startup")
    async def startup_event():
        logging.info("Application startup, initializing resources...")
        
    # check which database is connected
    @app.on_event("startup")
    async def startup_event():
        logging.info("Application startup, initializing resources...")
        print(engine.url.database)
        print(engine.url.username)
        print(engine.url.password)
        print(engine.url.host)
        print(engine.url.port)
        # print(engine.url.drivername)
        # print(engine.url.query)

    @app.on_event("shutdown")
    async def shutdown_event():
        logging.info("Application shutdown, cleaning up resources...")


    return app

myapp = create_app()

# Running the app with Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(myapp, host="0.0.0.0", port=8000)