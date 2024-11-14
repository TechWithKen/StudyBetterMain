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

def read_pdf(file, max_pages=100):
    """Read text from the first 100 pages of a PDF, using OCR for image pages."""
    text = []
    # Use the file object if directly passed from Django
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(min(max_pages, doc.page_count)):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        if page_text:
            text.append(page_text)
        else:
            pix = page.get_pixmap()
            image_data = pix.tobytes("png")
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

def read_file(file):
    """Determine file type and read content accordingly."""
    file_name = file.name if hasattr(file, 'name') else file  # Check for file-like object
    
    if file_name.endswith('.pdf'):
        # If it's an uploaded file, use it directly
        return read_pdf(file)
    elif file_name.endswith('.docx'):
        return read_docx(file)
    else:
        raise ValueError("Unsupported file type. Please use PDF or DOCX.")



def get_content(file_path):
    """Wrapper function to read and extract content from a file path."""
    try:
        content = read_file(file_path)
        return content  # Return the full extracted content
    except Exception as e:
        print(f"Error: {e}")
        return None
