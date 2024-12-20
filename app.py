#!/usr/bin/env python3

#  Copyright 2024 Code Inc. <https://www.codeinc.co>
#
#  Use of this source code is governed by an MIT-style
#  license that can be found in the LICENSE file or at
#  https://opensource.org/licenses/MIT.

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pymupdf
from models import ExtractResponse

app = FastAPI()

@app.get("/health")
async def health():
    return JSONResponse(content={"status": "up", "timestamp": datetime.now().isoformat()})


@app.post("/extract", response_model=ExtractResponse)
async def extract(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")

    pdf_bytes = await file.read()
    try:
        # Open the PDF with PyMuPDF
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        print(doc)
        with doc:
            pages_output = []

            # Iterate through the pages and extract text
            i = 1
            for page in doc:
                pages_output.append({
                    "page_number": i,
                    "text": (page.get_text() or "")
                })

            return {"pages": pages_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
