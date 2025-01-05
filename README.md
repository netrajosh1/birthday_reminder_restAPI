# birthday_reminder_restAPI

# Birthday Calendar API

This is a RESTful API built with FastAPI that allows you to manage and view birthdays. It supports adding, deleting, and retrieving birthdays, including upcoming birthdays and birthdays for a specific month. It also includes the ability to parse birthdays from uploaded text files and search for birthdays by name.

## Features

*   **Add Birthday:** Add a new birthday to the calendar with name, month, day, and an optional year and message.
*   **Delete Birthday:** Remove a birthday from the calendar by name, month, and day.
*   **Get Upcoming Birthdays:** Retrieve the next 10 upcoming birthdays in chronological order.
*   **Get Birthdays by Month:** Retrieve all birthdays for a specific month.
*   **Upload and Parse Text Files:** Upload a `.txt` file containing birthday information, and the API will parse and add the birthdays to the calendar. Supports "Happy Birthday", "Happy bday", "bday", and "birthday" with names and M/D/YY dates.
*   **Search by Name:** When uploading a text file, specify a list of names to search for, and only birthdays for those names will be added.

## Technologies Used

*   Python
*   FastAPI
*   Pydantic
*   datetime
*   Regular Expressions (re)
*   SwaggerAPI/Open API

## Setup

1.  **Clone the repository (if applicable):**

    ```bash
    git clone [https://your-repo-url.git](https://your-repo-url.git)
    cd birthday-calendar-api
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate      # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install fastapi uvicorn
    ```

## Running the API

1.  Navigate to the project directory in your terminal.

2.  Run the Uvicorn server:

    ```bash
    uvicorn pdf:app --reload
    ```

    (Replace `pdf` with the name of your Python file if it's different.)

3.  Open the interactive API documentation (Swagger UI) in your browser:

    ```
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    ```

## API Endpoints

*   **POST /birthdays/**: Add a birthday.
    *   Request Body: JSON with `name`, `month`, `day`, `year` (optional), and `message` (optional).
*   **DELETE /birthdays/**: Delete a birthday.
    *   Query Parameters: `name`, `month`, `day`.
*   **GET /birthdays/upcoming**: Get the next 10 upcoming birthdays.
*   **GET /calendar/{month}**: Get all birthdays for a given month.
    *   Path Parameter: `month` (1-12).
*   **POST /birthdays/from_text**: Add birthdays from an uploaded `.txt` file.
    *   Request Body: `file` (the `.txt` file) and `names` (a JSON array of names to search for).

## Example Usage (Adding a birthday)

```bash
curl -X POST \
  [invalid URL removed] \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John Doe",
    "month": 10,
    "day": 25,
    "year": 1990,
    "message":"Happy Birthday John!"
  }'
