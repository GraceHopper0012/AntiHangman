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
    guessresp = SPIEL.raten(buchstabe)
    
    if guessresp:
        if not guessresp.repeated:
            print("Richtig!\n")
        else:
            print("Schon geraten!")
    else:
        if not guessresp.repeated:
            print("Falsch!")
        else:
            print("Schon geraten!\n")

    
    
    gewonnen = SPIEL.ueberpruefe_gewonnen()
