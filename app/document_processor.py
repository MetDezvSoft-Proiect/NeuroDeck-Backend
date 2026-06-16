import os
import io
from pypdf import PdfReader

# Prag: daca un PDF are mai putin de 100 caractere per pagina in medie,
# il consideram scanat si folosim OCR
MIN_CHARS_PER_PAGE = 100

def _try_tesseract_path():
    """Seteaza calea catre Tesseract pe Windows daca nu e in PATH."""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except Exception:
        import pytesseract
        default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(default_path):
            pytesseract.pytesseract.tesseract_cmd = default_path

def _extrage_text_normal(file_path):
    """Extrage text direct din PDF (functioneaza doar pentru PDF-uri cu text real)."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def _extrage_text_ocr(file_path):
    """
    Renderizeaza fiecare pagina ca imagine si aplica OCR.
    Folosit pentru PDF-uri scanate sau cu continut predominant imagini.
    Necesita Tesseract instalat (https://github.com/UB-Mannheim/tesseract/wiki).
    """
    try:
        import fitz  # pymupdf
        import pytesseract
        from PIL import Image

        _try_tesseract_path()

        # Detectam limbile disponibile
        try:
            limbi_disponibile = pytesseract.get_languages()
            lang = "ron+eng" if "ron" in limbi_disponibile else "eng"
        except Exception:
            lang = "eng"

        print(f"OCR activ - limba: {lang}")

        doc = fitz.open(file_path)
        text = ""
        for i, page in enumerate(doc):
            print(f"  OCR pagina {i + 1}/{len(doc)}...")
            mat = fitz.Matrix(300 / 72, 300 / 72)
            pix = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            page_text = pytesseract.image_to_string(img, lang=lang)
            if page_text.strip():
                text += page_text + "\n"
        doc.close()
        return text

    except ImportError as e:
        raise RuntimeError(
            f"Dependinta lipsa pentru OCR: {e}. "
            "Ruleaza: pip install pymupdf pytesseract pillow"
        )
    except Exception as e:
        if "tesseract" in str(e).lower() or "not found" in str(e).lower():
            raise RuntimeError(
                "Tesseract OCR nu este instalat sau nu e in PATH. "
                "Descarca de la: https://github.com/UB-Mannheim/tesseract/wiki "
                "si asigura-te ca bifezi limba Romanian la instalare."
            )
        raise

def _este_pdf_scanat(file_path):
    """Returneaza True daca PDF-ul are prea putin text (probabil scanat)."""
    try:
        reader = PdfReader(file_path)
        if not reader.pages:
            return False
        total_chars = sum(len(page.extract_text() or "") for page in reader.pages)
        avg = total_chars / len(reader.pages)
        return avg < MIN_CHARS_PER_PAGE
    except Exception:
        return False

def extrage_text_din_pdf(file_path):
    """
    Extrage text dintr-un singur fisier PDF.
    Detecteaza automat daca e necesar OCR.
    """
    if _este_pdf_scanat(file_path):
        print(f"PDF scanat detectat: '{os.path.basename(file_path)}' - se aplica OCR...")
        return _extrage_text_ocr(file_path)
    else:
        return _extrage_text_normal(file_path)

def extrage_text_din_toate_pdf(folder_path):
    """Citeste toate fisierele PDF dintr-un folder si returneaza textul combinat."""
    text_complet = ""

    if not os.path.exists(folder_path):
        print(f"Eroare: Folderul '{folder_path}' nu exista.")
        return None

    fisiere_pdf = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not fisiere_pdf:
        print(f"Nu s-au gasit fisiere PDF in '{folder_path}'.")
        return None

    for fisier in fisiere_pdf:
        cale_completa = os.path.join(folder_path, fisier)
        print(f"Procesez: {fisier}")
        try:
            text = extrage_text_din_pdf(cale_completa)
            if text:
                text_complet += text + "\n"
        except RuntimeError:
            raise
        except Exception as e:
            print(f"Eroare la citirea {fisier}: {e}")

    return text_complet if text_complet.strip() else None

def extrage_text_dintr_un_pdf(cale_pdf):
    """Extrage text dintr-un singur fisier PDF (compatibilitate cu codul vechi)."""
    return extrage_text_din_pdf(cale_pdf)

def imparte_text_in_bucati(text, dimensiune_chunk=4000):
    """
    Imparte un text urias in bucati mai mici (chunks).
    Incearca sa nu taie in mijlocul unui paragraf.
    """
    if len(text) <= dimensiune_chunk:
        return [text]

    bucati = []
    start = 0
    while start < len(text):
        end = start + dimensiune_chunk
        if end < len(text):
            newline_pos = text.rfind("\n", start, end)
            if newline_pos > start:
                end = newline_pos + 1
        bucati.append(text[start:end])
        start = end
    return bucati
