from hangman import HangmanSpiel

gewonnen = False
SPIEL = HangmanSpiel()
falsche = 0
print("Gib immer nur einen Buchstaben ein!")
while not gewonnen:
    print(SPIEL.erstelle_overlay())
    if len(SPIEL.falsch_geraten) >= 10:
        print("Du hast verloren!")
        # break
    buchstabe = input("\nWas rätst du? ")
    richtig = SPIEL.raten(buchstabe)
    
    if richtig:
        print("Richtig!\n")
    else:
        print("Falsch!\n")
    
    
    gewonnen = SPIEL.ueberpruefe_gewonnen()
