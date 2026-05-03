def parseaza_flashcards_din_text(text_brut):
    flashcards = []
    linii = text_brut.split('\n')
    q_curent = None
    
    for linie in linii:
        linie = linie.strip()
        if linie.startswith('Q:'):
            q_curent = linie[2:].strip()
        elif linie.startswith('A:') and q_curent:
            a_curent = linie[2:].strip()
            flashcards.append({"intrebare": q_curent, "raspuns": a_curent})
            q_curent = None
            
    return flashcards