from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add")
async def add(
    request: Request,
    name: str = Form(...),
    position: str = Form(...),
    office: str = Form(...),
):
    print(name, position, office, sep="~")
    return RedirectResponse(
        url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})
