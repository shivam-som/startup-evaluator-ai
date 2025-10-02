from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import pathlib
from backend.my_workflow import workflow
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/chat")
async def get_chat_msgs():
    return {"message": "hi from GET"}

@app.post("/api/chat")
async def post_chat_msgs(request: Request):
    body = await request.json()
    idea = body.get("idea", "")

    async def stream():
        state = {"idea": idea}
        async for event in workflow.astream(state):
            for node, output in event.items():
                yield f"data: [{node}] {output.get(node, '')}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream")

@app.put("/api/chat")
async def put_chat_msgs(request: Request):
    return {"message": "hi from PUT", "you_sent": request}

@app.delete("/api/chat")
async def delete_chat_msgs():
    return {"message": "hi from DELETE"}


frontend_dir = pathlib.Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
