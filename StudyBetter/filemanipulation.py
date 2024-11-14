import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from docx import Document


def extract_text_from_image(image_data):
    """Extract text from an image using OCR."""
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text

def read_pdf(file_path, max_pages=100):
    """Read text from the first 100 pages of a PDF, using OCR for image pages."""
    text = []
    doc = fitz.open(file_path)
    for page_num in range(min(max_pages, doc.page_count)):
        page = doc.load_page(page_num)
        # Check if page contains text
        if page.get_text("text"):
            text.append(page.get_text("text"))
        else:
            # If no text, assume it's an image and extract text using OCR
            pix = page.get_pixmap()
            image_data = pix.tobytes("png")  # Convert to PNG bytes
            text.append(extract_text_from_image(image_data))
    doc.close()
    return "\n".join(text)

def read_docx(file_path):
    """Read text from a DOCX file."""
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)

def read_file(file_path):
    """Determine file type and read content accordingly."""
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.docx'):
        return read_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Please use PDF or DOCX.")


def get_content(file_path):
    content = ""  # Replace with your file path
    try:
        content = read_file(file_path)
        return content  # Print the first 1000 characters of the text
    except Exception as e:
        print(f"Error: {e}")
