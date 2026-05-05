import os
from pypdf import PdfReader

def extrage_text_din_toate_pdf(folder_path):
    """Citeste toate fisierele PDF dintr-un folder si returneaza textul combinat."""
    text_complet = ""
    
    if not os.path.exists(folder_path):
        print(f"❌ Eroare: Folderul '{folder_path}' nu exista.")
        return None
        
    fisiere_pdf = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not fisiere_pdf:
        print(f"⚠️ Nu s-au gasit fisiere PDF in '{folder_path}'.")
        return None
        
    for fisier in fisiere_pdf:
        cale_completa = os.path.join(folder_path, fisier)
        print(f"📄 Procesez fisierul: {fisier}")
        try:
            reader = PdfReader(cale_completa)
            for pagina in reader.pages:
                text_extras = pagina.extract_text()
                if text_extras:
                    text_complet += text_extras + "\n"
        except Exception as e:
            print(f"❌ Eroare la citirea {fisier}: {e}")
            
    return text_complet

def extrage_text_dintr_un_pdf(cale_pdf):
    """Extrage text dintr-un singur fisier PDF."""
    if not os.path.exists(cale_pdf):
        print(f"❌ Eroare: Fisierul '{cale_pdf}' nu exista.")
        return None
    
    text_complet = ""
    try:
        reader = PdfReader(cale_pdf)
        for pagina in reader.pages:
            text_extras = pagina.extract_text()
            if text_extras:
                text_complet += text_extras + "\n"
    except Exception as e:
        print(f"❌ Eroare la citirea PDF: {e}")
        return None
    
    return text_complet

def imparte_text_in_bucati(text, dimensiune_chunk=4000):
    """
    Imparte un text urias in bucati mai mici (chunks).
    Modelul Llama 3 proceseaza optim in jur de 4000-5000 de caractere per request.
    """
    bucati = []
    # Parcurgem textul din 4000 in 4000 de caractere
    for i in range(0, len(text), dimensiune_chunk):
        bucati.append(text[i : i + dimensiune_chunk])
    return bucati