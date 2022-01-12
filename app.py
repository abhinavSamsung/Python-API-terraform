from fastapi import FastAPI
from routes.posts import router as PostRouter
import uvicorn
app = FastAPI()

@app.get('/', tags=["Root"])
async def read_root():
    return {"message": "Welcome to the"}

app.include_router(PostRouter, tags=["TerraformApp"], prefix="/terraform-app")

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True, debug=True, workers=3)


