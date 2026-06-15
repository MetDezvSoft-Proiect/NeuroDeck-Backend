"""Teste unitare pentru parserul de flashcards (app/utils.py)."""
from app.utils import parseaza_flashcards_din_text


def test_parseaza_o_pereche():
    text = "Q: Ce este Python?\nA: Un limbaj de programare"
    rezultat = parseaza_flashcards_din_text(text)
    assert rezultat == [{"intrebare": "Ce este Python?", "raspuns": "Un limbaj de programare"}]


def test_parseaza_mai_multe_perechi():
    text = (
        "Q: Intrebare 1\nA: Raspuns 1\n"
        "Q: Intrebare 2\nA: Raspuns 2\n"
    )
    rezultat = parseaza_flashcards_din_text(text)
    assert len(rezultat) == 2
    assert rezultat[1] == {"intrebare": "Intrebare 2", "raspuns": "Raspuns 2"}


def test_ignora_text_fara_format():
    rezultat = parseaza_flashcards_din_text("Text oarecare fara intrebari sau raspunsuri")
    assert rezultat == []


def test_raspuns_fara_intrebare_este_ignorat():
    # Un 'A:' fara un 'Q:' inainte nu produce flashcard
    rezultat = parseaza_flashcards_din_text("A: Raspuns orfan")
    assert rezultat == []


def test_ignora_spatii_in_plus():
    text = "Q:   Intrebare cu spatii   \nA:   Raspuns cu spatii   "
    rezultat = parseaza_flashcards_din_text(text)
    assert rezultat == [{"intrebare": "Intrebare cu spatii", "raspuns": "Raspuns cu spatii"}]
