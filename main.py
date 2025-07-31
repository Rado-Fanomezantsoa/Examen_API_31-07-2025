from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse
from typing import List
from pydantic import BaseModel

app = FastAPI()

class EventModel(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str

events_store: List[EventModel] = []

def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted

@app.get("/")
def root(request: Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers not in ["text/plain" or "text/html"]:
        return JSONResponse({
            "error": "Unsupportable"
        }, status_code=400)

    api_secret = request.headers.get("x-api-key")
    if api_secret != "12345678":
        return JSONResponse({
            "error": "Cle API n'est pas reconnue"
        }, status_code=403)


    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(content=html_content, status_code=200, media_type="text/html")

@app.get("/events")
async def get_events(request: Request):
    # Vérifier l'en-tête Accept
    accept_header = request.headers.get("accept", "").lower()
    if accept_header not in ["application/json"]:
        return JSONResponse(
            content={"error": "Unsupported Accept header. Only 'application/json' is supported for this endpoint."},
            status_code=400
        )

    # Vérifier l'en-tête x-api-key
    api_key = request.headers.get("x-api-key")
    if api_key != "12345678":
        return JSONResponse(
            content={"error": "Unrecognized API key. The provided x-api-key is invalid."},
            status_code=403
        )

    return JSONResponse(content=serialized_stored_events(), status_code=200)

@app.post("/events")
async def create_events(request: Request, events: List[EventModel]):
    accept_header = request.headers.get("accept", "").lower()
    if accept_header not in ["application/json"]:
        return JSONResponse(
            content={"error": "Unsupported Accept header. Only 'application/json' is supported for this endpoint."},
            status_code=400
        )

    api_key = request.headers.get("x-api-key")
    if api_key != "12345678":
        return JSONResponse(
            content={"error": "Unrecognized API key. The provided x-api-key is invalid."},
            status_code=403
        )
    events_store.extend(events)
    return JSONResponse(content=serialized_stored_events(), status_code=201)

@app.put("/events")
async def update_events(request: Request, events: List[EventModel]):
    accept_header = request.headers.get("accept", "").lower()
    if accept_header not in ["application/json"]:
        return JSONResponse(
            content={"error": "Unsupported Accept header. Only 'application/json' is supported for this endpoint."},
            status_code=400
        )

    api_key = request.headers.get("x-api-key")
    if api_key != "12345678":
        return JSONResponse(
            content={"error": "Unrecognized API key. The provided x-api-key is invalid."},
            status_code=403
        )

    for new_event in events:
        for i, existing_event in enumerate(events_store):
            if existing_event.name == new_event.name:

                events_store[i] = new_event
                break
        else:
            events_store.append(new_event)

    return JSONResponse(content=serialized_stored_events(), status_code=200)

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    with open("not_found.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(content=html_content, status_code=404, media_type="text/html")