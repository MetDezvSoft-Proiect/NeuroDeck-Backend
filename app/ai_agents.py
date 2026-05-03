import ollama
from sentence_transformers import SentenceTransformer, util

print("⏳ Se incarca modelul NLP pentru evaluare...")
evaluator_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def genereaza_flashcards(text_suport, numar_intrebari):
    prompt = f"""
    Esti un asistent educational expert. Analizeaza urmatorul text si genereaza EXACT {numar_intrebari} intrebari esentiale cu raspunsuri scurte.
    REGULA STRICTA: EXCLUSIV in limba romana! 
    Returneaza STRICT {numar_intrebari} perechi de intrebari, in formatul de mai jos:
    Q: [Intrebare]
    A: [Raspuns]
    
    Text:
    {text_suport}
    """
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        print(f"❌ Eroare LLM: {e}")
        return None

def evalueaza_raspuns(raspuns_corect, raspuns_student, nivel_severitate):
    embedding_corect = evaluator_model.encode(raspuns_corect, convert_to_tensor=True)
    embedding_student = evaluator_model.encode(raspuns_student, convert_to_tensor=True)
    
    similaritate = util.cos_sim(embedding_corect, embedding_student).item()
    scor_brut = max(0, similaritate * 100)
    
    # Stabilim pragul minim in functie de severitate
    if nivel_severitate == 1:
        prag_minim = 30  # Usor
    elif nivel_severitate == 2:
        prag_minim = 40  # Mediu
    else:
        prag_minim = 50  # Dur

    # Aplicam formula de penalizare si scalare
    if scor_brut < prag_minim:
        scor_final = 0
    else:
        scor_final = ((scor_brut - prag_minim) / (100 - prag_minim)) * 100
        
    return int(scor_final)