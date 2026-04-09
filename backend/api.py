from fastapi import FastAPI,UploadFile,File
from source import scan_specific_repo, run_global_scan,scan_file_content,scan_text_input
from fastapi.middleware.cors  import CORSMiddleware
from pydantic import BaseModel

class TextScanRequest(BaseModel):
    text:str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/scan/text")
def scan_text(data:TextScanRequest):
    results,error=scan_text_input(data.text)
    if error:
        return {"error":error}
    return {"results": results,
                "error":None
                }

@app.post("/scan/file")
def scan_file(file: UploadFile = File(...)):
    try:
        content = file.file.read().decode("utf-8", errors="ignore")

        results, error = scan_file_content(content, file.filename)

        if error:
            return {
                "results":[],
                "error": error}

        return {"results": results,
                "error":None}

    except Exception as e:
        return {"error": str(e)}

@app.post("/scan/repo")
def scan_repo(data: dict):
    repo_url = data.get("repo_url")

    results, error = scan_specific_repo(repo_url)

    if error:
        return {
                "results":[],
                "error": error}

    return {"results": results,
                "error":None
                }


@app.post("/scan/global")
def scan_global(data: dict):
    try:
        limit = int(data.get("limit", 20))

        results, error = run_global_scan(limit)

        if error:
            return {"error": error}

        return {"results": results,
                "error":None
                }

    except Exception as e:
        print("ERROR:", e)   # 🔥 shows real issue in terminal
        return {"error": str(e)}