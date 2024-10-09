import os

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.0.130:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate/")
async def translate_local(file: UploadFile = File(...)):
    input_pdf_data = await file.read()

    result_pdf = input_pdf_data  # Replace this with your translation logic
    
    if result_pdf is None:
        return JSONResponse(status_code=400, content={"message": "Translation failed"})

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file.filename)

    with open(output_path, "wb") as f:
        f.write(result_pdf)

    return JSONResponse(
        status_code=200, content={"message": f"File saved at {output_path}"}
    )
    
@app.get("/download/{filename}")
async def download(filename: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    if not os.path.exists(output_path):
        return JSONResponse(status_code=404, content={"message": "File not found"})

    return FileResponse(output_path, media_type="application/pdf", filename=filename)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)