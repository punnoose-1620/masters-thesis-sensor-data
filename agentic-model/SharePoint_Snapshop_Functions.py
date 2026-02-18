# Functions to read files from Sharepoint Snapshot
import os
import csv
import docx
import pypdf
import openpyxl
import requests
import configparser
from PIL import Image
import pytesseract as pt
from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union

class SharePoint_Snapshop_Functions(BaseModel):

    def get_file_reader_instances(self):
        return {
            "pdf": self.read_pdf,
            "csv": self.read_csv,
            "xlsx": self.read_excel,
            "xlsm": self.read_excel,
            "docx": self.read_docx,
            "url": self.read_url,
            "dbc": self.read_dbc,
            "ini": self.read_ini,
            "png": self.read_image,
            "jpg": self.read_image,
            "jpeg": self.read_image,
            "gif": self.read_image,
            "bmp": self.read_image,
            "tiff": self.read_image,
            "webp": self.read_image,
            "ico": self.read_image,
        }
    
    ## Function to get file descriptions for SharePoint Snapshot
    @classmethod
    def get_file_descriptions(self):
        return ''

    ## Function to get the entire architecture
    @classmethod
    def get_architecture(self):
        """
        Returns a list of absolute paths for all files in the SharepointSnapshot folder.
        """
        base_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "SharepointSnapshot"))
        file_paths = []
        for root, _, files in os.walk(base_folder):
            for file in files:
                relative_path = os.path.join(root, file).split('agentic-model\\')[1]
                file_paths.append(f".\\{relative_path}")
        return file_paths

    ## Final Reader Function
    @classmethod
    def read_file(self, file_path: str, **kwargs: Any) -> Any:
        """
        Route to the right reader by file extension. For URLs pass a url string to read_url().
        """
        ext = file_path.strip().split(".")[-1].lower()
        READERS = self.get_file_reader_instances()
        if ext not in READERS:
            raise ValueError(f"No reader for extension '.{ext}'. Supported: {list(READERS.keys())}")
        return READERS[ext](file_path, **kwargs)
    
    ## Function to read PDF Files and return content
    def read_pdf(self, file_path: str) -> str:
        """Read a PDF and return text. Requires: pypdf"""
        if pypdf is None:
            raise ImportError("read_pdf requires pypdf. Install with: pip install pypdf")
        reader = pypdf.PdfReader(file_path)
        return "\n".join((p.extract_text() or "" for p in reader.pages)).strip()

    ## Function to read CSV Files and return content
    def read_csv(self, file_path: str, delimiter: str = ",", as_dict: bool = True) -> Union[List[Dict[str, str]], str]:
        """Read CSV; returns list of dicts by default or raw string if as_dict=False."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            if not as_dict:
                return f.read()
            return list(csv.DictReader(f, delimiter=delimiter))

    ## Function to read Excel Files (xlsx, xlsm) and return content
    def read_excel(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Read xlsx/xlsm; returns {sheet_name: [row_dict, ...]}. Requires: openpyxl"""
        if openpyxl is None:
            raise ImportError("read_xlsx requires openpyxl. Install with: pip install openpyxl")
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        out = {}
        for sheet in wb.worksheets:
            name = sheet.title
            if sheet_name is not None and name != sheet_name:
                continue
            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                out[name] = []
                continue
            headers = [str(h) if h is not None else "" for h in rows[0]]
            out[name] = [dict(zip(headers, row)) for row in rows[1:]]
        wb.close()
        return out

    ## Function to read Word Files and return content
    def read_docx(self, file_path: str) -> str:
        """Read docx and return text (paragraphs + table rows). Requires: python-docx"""
        if docx is None:
            raise ImportError("read_docx requires python-docx. Install with: pip install python-docx")
        doc = docx.Document(file_path)
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(c.text.strip() for c in row.cells))
        return "\n".join(parts).strip()

    ## Function to read URL Files and return content
    def read_url(self, url: str, as_text: bool = True) -> Union[str, bytes]:
        """Fetch URL content; returns text by default. Requires: requests"""
        if requests is None:
            raise ImportError("read_url requires requests. Install with: pip install requests")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text if as_text else r.content

    ## Function to read DBC Files and return content
    def read_dbc(self, file_path: str) -> str:
        """Read DBC file as raw text."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    ## Function to read INI Files and return content
    def read_ini(self, file_path: str) -> Dict[str, Dict[str, str]]:
        """Read INI config; returns {section: {key: value}}."""
        parser = configparser.ConfigParser()
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            parser.read_file(f)
        return {sec: dict(parser[sec]) for sec in parser.sections()}

    ## Function to read Image Files and return content
    def read_image(self, file_path: str, extract_text: bool = False) -> Dict[str, Any]:
        """Read image metadata; optionally OCR text. Returns dict with path, format, size, mode, and optionally 'text'. Requires: Pillow; OCR: pytesseract."""
        img = Image.open(file_path)
        img.load()
        info = {"path": os.path.abspath(file_path), "format": img.format, "size": img.size, "mode": img.mode}
        if extract_text:
            info["text"] = (pt.image_to_string(img).strip() if pt else "") or ""
        return info

# Testing Functions
filePaths = SharePoint_Snapshop_Functions.get_architecture()
filetypeCount = {}
for filePath in filePaths:
    extension = filePath.split('.')[-1]
    if extension not in filetypeCount:
        filetypeCount[extension] = 1
    else:
        filetypeCount[extension] += 1
    print(filePath)
print('\nFiletype Count:')
for extension, count in filetypeCount.items():
    print(f"{extension}: {count}")