import os
import math
from document_processor import extrage_text_din_toate_pdf, imparte_text_in_bucati
from ai_agents import genereaza_flashcards, evalueaza_raspuns
from utils import parseaza_flashcards_din_text

def start_sesiune():
    folder_pdf = r"C:\Users\Adrian\Neurodeck\Test_pdf" 
    
    print("\n" + "="*50)
    print(" 🧠 BINE AI VENIT IN NEURODECK ")
    print("="*50)
    
    # 1. Numar intrebari & Severitate
    try:
        numar_intrebari = int(input("\nCâte întrebări dorești să generezi din materialele tale? (ex: 5): "))
    except ValueError:
        print("❌ Te rog sa introduci un numar valid.")
        return

    print("\nNiveluri de severitate pentru evaluare:")
    print("1 - Ușor  (Acceptă idei parțiale, bun pentru recapitulare rapidă)")
    print("2 - Mediu (Echilibrat, ignoră lipsa detaliilor minore)")
    print("3 - Dur   (Necesită o potrivire semantică foarte precisă)")
    
    try:
        severitate = int(input("Alege severitatea (1/2/3): "))
        if severitate not in [1, 2, 3]:
            print("⚠️ Alegere invalidă. S-a setat implicit pe Mediu (2).")
            severitate = 2
    except ValueError:
        print("⚠️ Intrare invalidă. S-a setat implicit pe Mediu (2).")
        severitate = 2

    # 2. Extragerea Textului
    print("\nSe extrage textul din documentele din folder...")
    text_document = extrage_text_din_toate_pdf(folder_pdf)
    
    if not text_document:
        return

    # 3. NOU: CHUNKING (Impartim textul in felii)
    bucati_text = imparte_text_in_bucati(text_document, dimensiune_chunk=4000)
    numar_total_chunks = len(bucati_text)
    
    print(f"\n📚 Textul extras a fost impartit in {numar_total_chunks} segmente pentru a nu bloca AI-ul.")

    # Calculam cate intrebari cerem per segment (rotunjit in sus)
    intrebari_per_chunk = math.ceil(numar_intrebari / numar_total_chunks)
    if intrebari_per_chunk < 1: 
        intrebari_per_chunk = 1

    toate_flashcards_generate = []

    print(f"⏳ Se generează întrebările. Te rugăm să aștepți...\n")
    
    # Trimitem fiecare segment catre Llama 3
    for i, chunk in enumerate(bucati_text, 1):
        # Ne oprim daca am adunat deja numarul total de intrebari dorit
        if len(toate_flashcards_generate) >= numar_intrebari:
            break
            
        print(f"  -> Llama 3 analizeaza segmentul {i}/{numar_total_chunks}...")
        flashcards_text = genereaza_flashcards(chunk, intrebari_per_chunk)
        
        if flashcards_text:
            flashcards_parsate = parseaza_flashcards_din_text(flashcards_text)
            toate_flashcards_generate.extend(flashcards_parsate)
        else:
            print(f"  ⚠️ Segmentul {i} a intampinat o eroare, trecem mai departe.")

    # Ne asiguram ca avem EXACT numarul cerut de utilizator (taiem surplusul daca exista)
    flashcards_finale = toate_flashcards_generate[:numar_intrebari]
    
    if not flashcards_finale:
        print("❌ Nu s-au putut genera intrebari. Incearca sa maresti cantitatea de text in PDF-uri.")
        return

    print("\n" + "="*50)
    print(" 📝 INCEPE SESIUNEA DE TESTARE ")
    print("="*50 + "\n")
    #test
    intrebari_corecte = 0
    rezultate_finale = [] 

    numar_efectiv_intrebari = len(flashcards_finale)

    # 4. Desfasurarea testului
    for index, fc in enumerate(flashcards_finale, 1):
        print(f"[{index}/{numar_efectiv_intrebari}] Intrebare: {fc['intrebare']}")
        raspunsul_tau = input("Răspunsul tău: ")
        
        scor = evalueaza_raspuns(fc['raspuns'], raspunsul_tau, severitate)
        
        este_corect = scor >= 70
        if este_corect:
            intrebari_corecte += 1
            status = "✅ CORECT"
        else:
            status = "❌ INCORECT"

        rezultate_finale.append({
            "intrebare": fc['intrebare'],
            "raspuns_corect": fc['raspuns'],
            "raspunsul_tau": raspunsul_tau,
            "scor": scor,
            "status": status
        })
        
        print(f"Scorul tau de acuratete: {scor}% -> {status}")
        print("-" * 50 + "\n")

    # 5. Raport Final
    print("\n" + "="*50)
    print(" 📊 REZUMATUL SESIUNII ")
    print("="*50)
    
    for index, rez in enumerate(rezultate_finale, 1):
        print(f"\nQ{index}: {rez['intrebare']}")
        print(f"Răspunsul tău: {rez['raspunsul_tau']} (Acuratețe: {rez['scor']}%) - {rez['status']}")
        print(f"Răspunsul așteptat (AI): {rez['raspuns_corect']}")

    if numar_efectiv_intrebari > 0:
        nota = (intrebari_corecte / numar_efectiv_intrebari) * 10
    else:
        nota = 0.0

    print("\n" + "*"*50)
    print(f" Severitate selectata: Nivelul {severitate}")
    print(f" Ai raspuns corect la: {intrebari_corecte} din {numar_efectiv_intrebari} intrebari (Peste 70% acuratete)")
    print(f" NOTA FINALA: {nota:.2f} / 10")
    print("*"*50 + "\n")

if __name__ == "__main__":
    start_sesiune()