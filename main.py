from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
from contextlib import asynccontextmanager

import database
from models import Blog
from schemas import BlogSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/blogs")
async def create_blog(
    request: Request,
    blog_item: BlogSchema,
    session: Session = Depends(database.get_session),
):
    try:
        blog = Blog(title=blog_item.title, body=blog_item.body, author=blog_item.author)

        session.add(blog)
        session.commit()
        session.refresh(blog)

        return JSONResponse(
            content={
                "success": True,
                "data": jsonable_encoder(blog),
                "message": "Blog is successfully created",
            },
            status_code=status.HTTP_201_CREATED,
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "data": {}, "message": "Invalid data"},
        )


@app.get("/blogs")
async def get_blogs(
    request: Request,
    id: int | None = None,
    session: Session = Depends(database.get_session),
):
    try:
        if id:
            blogs = session.exec(select(Blog).where(Blog.id == id)).one()
        else:
            blogs = session.exec(select(Blog)).all()

        return JSONResponse(
            content={
                "success": True,
                "data": jsonable_encoder(blogs),
                "message": "Blogs are retrieved",
            },
            status_code=status.HTTP_200_OK,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "data": {}, "message": "Internal Server Error"},
        )


@app.put("/blogs")
async def update_blog(
    request: Request,
    blog_id: int,
    blog_item: BlogSchema,
    session: Session = Depends(database.get_session),
):
    try:
        blog = session.exec(select(Blog).where(Blog.id == blog_id)).one()
        for key, value in dict(blog_item).items():
            setattr(blog, key, value) if value else ...

        session.add(blog)
        session.commit()
        session.refresh(blog)

        return JSONResponse(
            content={
                "success": True,
                "data": jsonable_encoder(blog),
                "message": "Blog is updated",
            },
            status_code=status.HTTP_202_ACCEPTED,
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "data": {}, "message": "Internal Server Error"},
        )


@app.delete("/blogs")
async def delete_blog(
    request: Request,
    blog_id: int,
    session: Session = Depends(database.get_session),
):
    try:
        blog = session.exec(select(Blog).where(Blog.id == blog_id)).one()
        session.delete(blog)

        session.commit()

        return JSONResponse(
            content={
                "success": True,
                "data": jsonable_encoder(blog),
                "message": "Blog is deleted successfully",
            },
            status_code=status.HTTP_202_ACCEPTED,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "data": {}, "message": "Invalid data"},
        )
