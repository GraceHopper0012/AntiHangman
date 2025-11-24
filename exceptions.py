class KeinePositionUebrigError(Exception):
    """Wird geraised, wenn das Programm sich verspielt hat und keine Position mehr falsch ist"""
    def __init__(self, message="Es gibt keine Position mehr. Bitte melde diesen Fehler Felix, dankeschön!"):
        super().__init__(message)
