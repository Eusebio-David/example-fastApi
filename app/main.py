from fastapi import FastAPI
from . import models
from .database import engine
from.routers import post,user,auth,votes, likes
from .config import Setting
from fastapi.middleware.cors import CORSMiddleware



#models.Base.metadata.create_all(bind=engine)

origins=["https://www.google.com"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(likes.router)


#global variable to save my date
"""
my_posts =[{"title": "title of post 1",
            "content": "content of post 1",
            "id": 1},

            {"title": "favorite food",
            "content": "i like pizza",
            "id": 2}
            ]

#we search for a post by its id
def find_post(id:int):
    for i in my_posts:
        if i["id"]== id:
            return i

def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


"""



@app.get("/")
async def root():
    return {"message": "Hello, welcome to my blog"}




    

