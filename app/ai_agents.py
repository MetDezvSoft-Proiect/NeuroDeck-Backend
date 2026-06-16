import ollama
from sentence_transformers import SentenceTransformer, util
import os
import socket

_evaluator_model = None

def _get_evaluator():
    global _evaluator_model
    if _evaluator_model is None:
        print("Se incarca modelul NLP pentru evaluare...")
        _evaluator_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return _evaluator_model

def check_ollama_available():
    """Verifică dacă Ollama e accessible pe localhost:11434"""
    try:
        sock = socket.create_connection(("127.0.0.1", 11434), timeout=2)
        sock.close()
        print("Ollama e disponibil pe localhost:11434")
        return True
    except Exception:
        print("Ollama NU e disponibil. Voi folosi mock data pentru testing.")
        return False

OLLAMA_AVAILABLE = check_ollama_available()

def genereaza_flashcards(text_suport, numar_intrebari):
    """Generează flashcards din text. Dacă Ollama nu e disponibil, returnează date simulate."""
    prompt = f"""
    Esti un asistent educational expert. Analizeaza urmatorul text si genereaza EXACT {numar_intrebari} intrebari esentiale cu raspunsuri scurte.
    REGULA STRICTA: EXCLUSIV in limba romana! 
    Returneaza STRICT {numar_intrebari} perechi de intrebari, in formatul de mai jos:
    Q: [Intrebare]
    A: [Raspuns]
    
    Text:
    {text_suport}
    """
    
    if not OLLAMA_AVAILABLE:
        print("Folosesc mock flashcards pentru testing...")
        return generate_mock_flashcards(text_suport, numar_intrebari)
    
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        print(f"Eroare la Ollama: {e}")
        print("Revin la mock flashcards...")
        return generate_mock_flashcards(text_suport, numar_intrebari)

def generate_mock_flashcards(text_suport, numar_intrebari):
    """Generează flashcards simulate pentru testing când Ollama nu e disponibil."""
    # Extract first sentences as base for questions
    sentences = text_suport.split('.')[:numar_intrebari]
    
    mock_pairs = []
    for i, sentence in enumerate(sentences[:numar_intrebari], 1):
        sentence = sentence.strip()
        if sentence:
            question = f"Q: {sentence[:60]}?"
            answer = f"A: {sentence}"
            mock_pairs.append(f"{question}\n{answer}")
    
    # If we don't have enough questions, add default ones
    while len(mock_pairs) < numar_intrebari:
        i = len(mock_pairs) + 1
        mock_pairs.append(f"Q: Care este conceptul {i}?\nA: Răspuns pentru conceptul {i} din material.")
    
    return "\n\n".join(mock_pairs[:numar_intrebari])

def evalueaza_raspuns(raspuns_corect, raspuns_student, nivel_severitate):
    model = _get_evaluator()
    embedding_corect = model.encode(raspuns_corect, convert_to_tensor=True)
    embedding_student = model.encode(raspuns_student, convert_to_tensor=True)
    
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