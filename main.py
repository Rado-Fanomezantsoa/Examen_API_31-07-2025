from fastapi import FastAPI, Request, status
from starlette.responses import Response, JSONResponse
from typing import List
from pydantic import BaseModel

app = FastAPI()

@app.get("/ping")
def pingPong() :
    return Response(content="pong", status_code=200)



@app.get("/home")
def welcomeHome():
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(content=html_content, status_code=200, media_type="text/html")

@app.get("/")
async def catch_all():
    with open("notFound.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")


class Posts(BaseModel):
    Author: str
    title: str
    content: str
    creation_datetime: str

posts_store: List[Posts] = [];




@app.post("/posts", response_model=List[Posts], status_code=status.HTTP_201_CREATED)
async def create_players(posts: List[Posts]):
    existing_post = {post.title for post in posts_store}
    new_posts = []
    
    for post in posts:
        if post.title in existing_post:
            continue
        posts_store.append(post)
        new_posts.append(post)
        existing_post.add(post.title)

    if not new_posts:
        return posts_store
    else:
        return new_posts



@app.get("/posts", response_model=List[Posts], status_code=status.HTTP_200_OK)
async def get_players():
    return posts_store


@app.put("/players", response_model=List[Posts], status_code=status.HTTP_200_OK)
async def update_or_create_players(players: List[Posts]):
    updated = False
    new_post = []
    
    for post in players:
        existing_post = next((p for p in posts_store if p.title == post.title), None)
        if existing_post:
            if existing_post.name != post.name:
                existing_post.name = post.name
                updated = True
        else:
            posts_store.append(post)
            new_post.append(post)
    
    if updated or new_post:
        return posts_store 
    return posts_store
