from fastapi import FastAPI, HTTPException, Query, Body, UploadFile, Path, File  # Import UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, date, timedelta
import re

app = FastAPI(title="Birthday Calendar API", description="Manage and view birthdays.")


# Data Model
class Birthday(BaseModel):
    name: str = Field(..., description="Name of the person")
    month: int = Field(..., ge=1, le=12, description="Month of birthday (1-12)")
    day: int = Field(..., ge=1, le=31, description="Day of birthday (1-31)")
    year: Optional[int] = Field(None, description="Year of birth (optional)")
    message: Optional[str] = Field(None, description="Custom Birthday Message")


# In-memory calendar (replace with a database for production)
calendar: Dict[int, Dict[int, List[Birthday]]] = {}  # {month: {day: [Birthdays]}}


def get_calendar_day(month: int, day: int):
    """Retrieves the list of birthdays for a given month and day."""
    if month not in calendar:
        return None
    if day not in calendar[month]:
        return None
    return calendar[month][day]


# API Endpoints

@app.post("/birthdays/", response_model=Birthday, summary="Add a birthday to the calendar")
async def add_birthday(birthday: Birthday):
    if birthday.month not in calendar:
        calendar[birthday.month] = {}
    if birthday.day not in calendar[birthday.month]:
        calendar[birthday.month][birthday.day] = []
    calendar[birthday.month][birthday.day].append(birthday)
    return birthday

@app.delete("/birthdays/", summary="Delete a birthday from the calendar")
async def delete_birthday(name: str = Query(..., description="name of person to delete"),
                          month: int = Query(..., ge=1, le=12, description="Month of birthday (1-12)"),
                          day: int = Query(..., ge=1, le=31, description="Day of birthday (1-31)")):
    day_birthdays = get_calendar_day(month, day)
    if not day_birthdays:
        raise HTTPException(status_code=404, detail="No birthdays found on that day.")
    for birthday in day_birthdays:
        if birthday.name == name:
            day_birthdays.remove(birthday)
            return {"message": f"Birthday of {name} on {month}/{day} deleted."}

    raise HTTPException(status_code=404, detail=f"No birthday found for {name} on {month}/{day}.")

@app.get("/birthdays/upcoming", summary="Get the next 10 upcoming birthdays")
async def get_upcoming_birthdays():
    today = date.today()
    upcoming = []
    for _ in range(366): #look through next year
        current_date = today + timedelta(days=_)
        month = current_date.month
        day = current_date.day

        day_birthdays = get_calendar_day(month, day)
        if day_birthdays:
            for birthday in day_birthdays:
                upcoming.append({
                    "name": birthday.name,
                    "date": current_date.strftime("%m/%d/%Y"),
                    "message": birthday.message
                })
        if len(upcoming) >= 10:
            break
    return upcoming

@app.get("/calendar/{month}", summary="Get all birthdays for a given month", response_model=Dict[int, List[Birthday]])
async def get_birthdays_by_month(month: int = Path(..., ge=1, le=12, description="Month (1-12)")):
    if month not in calendar:
        raise HTTPException(status_code=404, detail=f"No birthdays found in month {month}")
    return calendar[month]


@app.post("/birthdays/from_text", summary="Add birthdays from uploaded txt file")
async def add_birthdays_from_text(file: UploadFile = File(...), names: List[str] = Body(...)): #Corrected line
    try:
        contents = await file.read()
        text = contents.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding. Please use UTF-8.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

    return add_birthdays_from_string(text, names)  # Call existing function



def add_birthdays_from_string(text: str, names: List[str]) -> Dict[str, str]:
    lines = text.splitlines()
    added_count = 0
    for line in lines:
        match = re.search(r"\b(happy birthday(?: to | of )?|happy bday )([^!]+?)\b.*?\b(\d{1,2}/\d{1,2}/\d{2})\b", line, re.IGNORECASE)
        if match:
            message_parts = match.groups()
            birthday_message = message_parts[0] + message_parts[1].strip() + message_parts[2].strip()
            name = message_parts[1].strip()
            if name in names: #check if name is in the list of names provided
                date_match = re.search(r"\b(\d{1,2}/\d{1,2}/\d{2})\b", line)
                if date_match:
                    date_str = date_match.group(1)
                    try:
                        date_obj = datetime.strptime(date_str, "%m/%d/%y").date()
                        birthday = Birthday(name=name, month=date_obj.month, day=date_obj.day,
                                            year=date_obj.year, message=birthday_message)
                        if birthday.month not in calendar:
                            calendar[birthday.month] = {}
                        if birthday.day not in calendar[birthday.month]:
                            calendar[birthday.month][birthday.day] = []
                        calendar[birthday.month][birthday.day].append(birthday)
                        added_count += 1
                    except ValueError:
                        print(f"Warning: Invalid date format: {date_str}")
    return {"message": f"{added_count} birthdays added from text."}