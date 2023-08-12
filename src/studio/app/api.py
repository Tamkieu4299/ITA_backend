from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .constants.config import settings
from .db.database import Base, engine
from .routers.audio_router import router as audio_router
from .routers.cv_router import router as cv_router
from .routers.generation_router import router as generation_router
from .routers.image_router import router as image_router
from .routers.interview_session_router import (
    router as interview_session_router,
)
from .routers.jd_router import router as jd_router
from .routers.question_router import router as question_router
from .routers.s3_router import router as s3_router
from .routers.text_router import router as text_router
from .routers.video_router import router as video_router
from .routers.answer_router import router as answer_router
from .routers.user_router import router as user_router
from .routers.auth_router import router as auth_router

Base.metadata.create_all(bind=engine)


PREFIX = f"/api/{settings.API_VERSION}/studio"

app = FastAPI(
    openapi_url=f"{PREFIX}/openapi.json",
    docs_url=f"{PREFIX}/docs",
    redoc_url=f"{PREFIX}/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(image_router, tags=["Image"], prefix=f"{PREFIX}/image")
app.include_router(video_router, tags=["Video"], prefix=f"{PREFIX}/video")
app.include_router(audio_router, tags=["Audio"], prefix=f"{PREFIX}/audio")
app.include_router(cv_router, tags=["CV"], prefix=f"{PREFIX}/cv")
app.include_router(jd_router, tags=["JD"], prefix=f"{PREFIX}/jd")
app.include_router(text_router, tags=["Text"], prefix=f"{PREFIX}/text")
app.include_router(
    question_router, tags=["Question"], prefix=f"{PREFIX}/question"
)
app.include_router(s3_router, tags=["S3"], prefix=f"{PREFIX}/s3")
app.include_router(
    generation_router, tags=["Generation"], prefix=f"{PREFIX}/generation"
)
app.include_router(answer_router, tags=["Answer"], prefix=f"{PREFIX}/answer")
app.include_router(
    interview_session_router,
    tags=["Interview Session"],
    prefix=f"{PREFIX}/interview_session",
)
app.include_router(user_router, tags=["User"], prefix=f"{PREFIX}/user")
app.include_router(auth_router, tags=["Auth"], prefix=f"{PREFIX}/auth")
