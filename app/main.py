from app.routes.task_routes import router as task_routes
from app.routes.user_routes import router as user_routes
from app.routes.auth_routes import router as auth_routes
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(auth_routes, prefix="/api")
app.include_router(user_routes, prefix="/api")
app.include_router(task_routes, prefix="/api")


@app.get("api/")
async def root():
    return {"message": "FastAPI ishlayapti "}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=3489)
