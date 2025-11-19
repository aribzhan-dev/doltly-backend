from fastapi import FastAPI
from app.routes.task_routes import router as task_routes
from app.routes.user_routes import router as user_routes
import uvicorn


app = FastAPI()
app.include_router(task_routes)
app.include_router(user_routes)

@app.get("/")
async def root():
    return {"message": "FastAPI ishlayapti "}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=9080)
