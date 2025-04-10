from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import docx

def extract_text_from_file(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    elif file.name.lower().endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)
