#!/usr/bin/env python3

#  Copyright (c) 2024 Code Inc. - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Visit <https://www.codeinc.co> for more information

import io
import pdfplumber
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
import nltk
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health():
    return JSONResponse(content={"status": "up", "timestamp": datetime.now().isoformat()})

@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    tokenize: Optional[bool] = Query(False, description="If true, return sentence tokenization.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")

    pdf_bytes = await file.read()
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages_output = []
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                page_dict = {
                    "page_number": page_num,
                    "text": text
                }
                if tokenize:
                    # Tokenize text into sentences
                    sentences = nltk.sent_tokenize(text)
                    page_dict["sentences"] = sentences
                pages_output.append(page_dict)

            return {"pages": pages_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
