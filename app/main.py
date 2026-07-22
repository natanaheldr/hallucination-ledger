from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.database import engine, Base
from app.routers import claims, sources


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Hallucination Ledger", version="0.1.0", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

app.include_router(claims.router)
app.include_router(sources.router)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/add", response_class=HTMLResponse)
def add_response_page(request: Request):
    return templates.TemplateResponse("add_response.html", {"request": request})


@app.get("/api/seed-demo")
def seed_demo():
    from app.seed_demo import seed_demo_data
    return seed_demo_data()


@app.get("/claims/{claim_id}", response_class=HTMLResponse)
def claim_detail_page(claim_id: int, request: Request):
    return templates.TemplateResponse("claim_detail.html", {"request": request, "claim_id": claim_id})
