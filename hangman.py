"""
Hangman-Spielmodul

Enthält Logik für ein Hangman-Spiel
"""

from random import randint
import sys, os
from collections import Counter
from exceptions import KeinePositionUebrigError

ZEILE_1 = ["", "", "  |", "  |--------|"]
ZEILE_2 = ["", "", "  |", "  |", "  |/", "  |/       O"]
ZEILE_3 = [
    "",
    "",
    "  |",
    "  |",
    "  |",
    "  |",
    "  |        |",
    "  |       /|",
    "  |       /|\\",
]
ZEILE_4 = [
    "",
    "",
    "  |",
    "  |",
    "  |",
    "  |",
    "  |",
    "  |",
    "  |",
    "  |       /",
    "  |       / \\",
]
ZEILE_5 = ["", "", "  |"]
ZEILE_6 = ["", "_____"]
HANGMANS = [ZEILE_1, ZEILE_2, ZEILE_3, ZEILE_4, ZEILE_5, ZEILE_6]
VOKALE = ["a", "e", "i", "o", "u", "ä", "ö", "ü", "à", "á", "â", "è", "é", "ê", "ò", "ó", "ô", "ì", "í", "î", "ù", "ú", "û"]


class HangmanSpiel:
    """
    Eine Klasse zur Verwaltung des Spiels Hangman.
    Attribute:
        wort (str): Das zu erratende Wort, in Kleinbuchstaben.
        falschgeraten (list): Liste der falsch geratenen Buchstaben.
        geraten (list): Liste der geratenen Buchstaben.
    Methoden:
        __init__(wort: str):
            Initialisiert das Spiel mit dem gegebenen Wort.
        raten(buchstabe: str) -> bool:
            Versucht, einen Buchstaben zu raten. Gibt True zurück, wenn der Buchstabe im Wort ist,
            False bei ungültigem oder bereits geratenem Buchstaben.
        falsch(buchstabe: str) -> None | bool:
            Fügt einen falsch geratenen Buchstaben zur Liste hinzu, falls noch nicht vorhanden.
            Gibt False zurück, wenn der Buchstabe bereits als falsch geraten wurde.
        male_hangman(falsche: int) -> str:
            Gibt eine String-Repräsentation des aktuellen Hangman-Zustands zurück, basierend auf der Anzahl der Fehlversuche.
        male_wort(trennung: str = '') -> str:
            Gibt das aktuelle Wort mit geratenen Buchstaben und Platzhaltern für nicht geratene Buchstaben zurück.
        ueberpruefe_gewonnen() -> bool:
            Überprüft, ob das gesamte Wort korrekt geraten wurde.
        erstelle_overlay() -> str:
            Erstellt eine textuelle Übersicht des aktuellen Spielstands, inklusive Wort, Hangman und falscher Buchstaben.
    """

    def __init__(self, wortliste = "wordlist-german.txt", wortlaenge: int = None):
        self.wort = ""
        self.falsch_geraten = []
        self.geraten = []
        if wortlaenge == None or wortlaenge > 7 or wortlaenge < 4:
            wortlaenge = randint(4,7)
        self.wortlaenge = wortlaenge
        self.positionen = ["_" for _ in range(self.wortlaenge)]
        
        if getattr(sys, 'frozen', False):
            # Wenn als .exe ausgeführt
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        dateipfad = os.path.join(base_path, os.path.join("resources", wortliste))
        with open(dateipfad, "r", encoding="utf-8") as f:
            self.wortliste = [line.strip().lower() for line in f.readlines()]
            neue_wortliste = []
            for wort in self.wortliste:
                if len(wort) == self.wortlaenge:
                    for vokal in VOKALE:
                        if vokal in wort:
                            neue_wortliste.append(wort)
                            break
            self.wortliste = neue_wortliste

    def ueberpruefe_passt_positionen(self, wort):
        for idx, position in enumerate(self.positionen):
            if position != "_":
                if position != wort[idx]:
                    return False
        
        for buchstabe in self.geraten:
            if not buchstabe in self.positionen:
                continue
            if buchstabe in wort:
                # einer der Buchstaben im Wort wurde bereits geraten
                for idx, wortstabe in enumerate(wort):
                    if wortstabe == buchstabe:
                        if self.positionen[idx] != wortstabe:
                            return False
        return True
                

    def finde_nicht_worte(self, buchstabe: str = None, nur_existenz_pruefen: bool = False):
        richtige = []
        for wort in self.wortliste:
            if len(wort.strip().lower()) != self.wortlaenge:
                continue
            gehtnich = False
            for stuchbabe in self.falsch_geraten:
                if stuchbabe in wort:
                    gehtnich = True
            if gehtnich:
                continue
            if buchstabe != None and buchstabe in wort:
                continue
            if not self.ueberpruefe_passt_positionen(wort):
                continue
            
            # wort ist zugelassen
            if nur_existenz_pruefen:
                return True
            richtige.append(wort)

        if nur_existenz_pruefen:
            return False
        else:
            return richtige
    
    def ueberpruefe_wort(self, wort):
        if type(wort) != str or wort == "" or len(wort) <= 3:
            return False
        return True
        
    def raten(self, buchstabe: str):
        if len(buchstabe) != 1:
            return False

        buchstabe = buchstabe.lower()
        if buchstabe in self.geraten:
            return False

        self.geraten.append(buchstabe)

        if self.finde_nicht_worte(buchstabe, True):
            print(f"Es gibt noch {len(self.finde_nicht_worte(buchstabe, False))} mögliche Wörter! (-x, weil ist halt so, kein Bock das zu fixen)")
            self.falsch(buchstabe)
            return False
        else:
            # self.positionen muss geändert werden, der User hat richtig geraten
            worte = self.finde_nicht_worte(nur_existenz_pruefen = False)
            positions_liste = self.finde_position(buchstabe, worte, self.check_freie_pos())
            for position in positions_liste[0]:
                self.positionen[position] = buchstabe
            return True
        
        
    def check_freie_pos(self):
        return [i for i, buchstabe in enumerate(self.positionen) if buchstabe == "_"]

    def falsch(self, buchstabe: str):
        buchstabe = buchstabe.lower()
        if buchstabe not in self.falsch_geraten:
            self.falsch_geraten.append(buchstabe)
            return True
        return False

    def male_hangman(self, falsche):
        hangman = ""
        for zeile in HANGMANS:
            try:
                hangman += zeile[falsche] + "\n"
            except IndexError:
                hangman += zeile[len(zeile) - 1] + "\n"
        return hangman.rstrip("\n")


    def finde_position(self, buchstabe, woerter, freie_pos):
        positionen=[]
        for wort in woerter:
            positionen.append([i for i, stuchbabe in enumerate(wort) if stuchbabe == buchstabe and i in freie_pos])

        gesamt_counter = Counter()
        for pos_liste in positionen:
            gesamt_counter.update(pos_liste)

        haeufigkeit_sortiert = [pos for pos, _ in gesamt_counter.most_common()]

        posl = []
        for pos in haeufigkeit_sortiert:
            # Zähle Wörter, die *nur* an dieser Position buchstabe enthalten
            nur_diese_pos = [pos_liste for pos_liste in positionen if pos_liste == [pos]]
            if nur_diese_pos:
                posl.append([pos])
        if len(posl) > 0:
            return posl

        if haeufigkeit_sortiert:
            return [haeufigkeit_sortiert]
        else:
            raise KeinePositionUebrigError

    def male_wort(self, trennung: str = ""):
        return trennung.join(self.positionen)

    def ueberpruefe_gewonnen(self):
        if "_" in self.positionen:
            return False
        return True

    def erstelle_overlay(self):
        overlay = (
            "Wort:\n"
            + self.male_wort("")
            + "\n\n"
            + self.male_hangman(len(self.falsch_geraten))
            + "\nFalsche Buchstaben: "
            + ", ".join(self.falsch_geraten)
        )
        return overlay
