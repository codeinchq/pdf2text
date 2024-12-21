#!/usr/bin/env python3

#  Copyright 2024 Code Inc. <https://www.codeinc.co>
#
#  Use of this source code is governed by an MIT-style
#  license that can be found in the LICENSE file or at
#  https://opensource.org/licenses/MIT.

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from datetime import datetime
import pymupdf
from models import ExtractResponse
import pdfplumber
import io
import os

app = FastAPI()
start_time = datetime.now()

@app.get("/health")
async def health():
    """
    Health check endpoint to verify the service is up and running.

    :return: JSON response with service status, uptime, version, and build ID
    """
    return {
        "status": "ok",
        "uptime": str(datetime.now() - start_time),
        "version": os.getenv("VERSION", "unknown"),
        "build_id": os.getenv("BUILD_ID", "unknown")
    }


@app.post("/extract/fast", response_model=ExtractResponse)
async def extract(
    file: UploadFile = File(...),
    first_page: int = Query(1, ge=1, description="The first page to extract."),
    last_page: int = Query(None, ge=1, description="The last page to extract."),
    password: str = Query(None, description="Password to unlock the PDF.")
):
    """
    Extract text from PDF pages using PyMuPDF.

    :param file: PDF file to extract text from
    :param first_page: First page to extract (default 1)
    :param last_page: Last page to extract (default last page)
    :param password: Password to unlock the PDF (default none)

    :return: Extracted text from each page
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")

    pdf_bytes = await file.read()
    try:
        # Open the PDF with PyMuPDF
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

        # Handle password-protected PDFs
        if password:
            if not doc.authenticate(password):
                raise HTTPException(status_code=401, detail="Incorrect password for the PDF.")

        # Default last page to the number of pages in the document
        last_page = last_page or doc.page_count

        if first_page < 1 or last_page > doc.page_count or first_page > last_page:
            raise HTTPException(status_code=400, detail="Invalid page range.")

        pages_output = []
        with doc:
            for i in range(first_page - 1, last_page):
                page = doc[i]
                pages_output.append({
                    "page_number": i + 1,
                    "text": page.get_text() or ""
                })

        return {"pages": pages_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/advanced", response_model=ExtractResponse)
async def extract_advanced(
    file: UploadFile = File(...),
    first_page: int = Query(1, ge=1, description="The first page to extract."),
    last_page: int = Query(None, ge=1, description="The last page to extract."),
    password: str = Query(None, description="Password to unlock the PDF.")
):
    """
    Extract text and tables from PDF pages using pdfplumber for better table extraction.

    :param file: PDF file to extract text and tables from
    :param first_page: First page to extract (default 1)
    :param last_page: Last page to extract (default last page)
    :param password: Password to unlock the PDF (default none)

    :return: Extracted text and tables from each page
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")

    pdf_bytes = await file.read()
    try:
        pages_output = []

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            # Handle password-protected PDFs
            if pdf.is_encrypted:
                if not password:
                    raise HTTPException(status_code=401, detail="PDF is password-protected.")
                pdf.decrypt(password)

            # Default last page to the number of pages in the document
            last_page = last_page or len(pdf.pages)

            if first_page < 1 or last_page > len(pdf.pages) or first_page > last_page:
                raise HTTPException(status_code=400, detail="Invalid page range.")

            for i in range(first_page - 1, last_page):
                page = pdf.pages[i]

                # Extract text
                text = page.extract_text() or ""

                # Extract tables
                tables = page.extract_tables()

                pages_output.append({
                    "page_number": i + 1,
                    "text": text,
                    "tables": tables
                })

        return {"pages": pages_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))