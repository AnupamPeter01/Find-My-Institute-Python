from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from database import SessionLocal, institutes_table
from starlette.requests import Request


app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



# Handle form submission
@app.post("/eligible_institutes", response_class=HTMLResponse)
async def eligible_institutes(
        request: Request,
        gender: str = Form(...),
        program_name: str = Form(...),
        seat_type: str = Form(...),
        rank: int = Form(...),
        db: Session = Depends(get_db)
):
    # Query the database for eligible institutes
    query = select(institutes_table.c.institute_name).where(
        and_(
            institutes_table.c.gender == gender,
            institutes_table.c.seat_type == seat_type,
            institutes_table.c.program_name == program_name,
            institutes_table.c.opening_rank <= rank,
            institutes_table.c.closing_rank >= rank
        )
    )
    result = db.execute(query).fetchall()

    institute_names = [row[0] for row in result]
    return templates.TemplateResponse(
        "results.html", {"request": request, "institutes": institute_names}
    )


@app.get("/institutes/{institute_id}")
def get_institute_by_id(institute_id: int, db: Session = Depends(get_db)):
    # Create a SELECT query for the student with the given ID
    stmt = select(institutes_table).where(institutes_table.c.id == institute_id)

    # Execute the query
    result = db.execute(stmt).mappings().fetchone()

    # If no student is found, raise an HTTP exception
    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result