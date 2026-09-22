class GuessResponse:
    def __init__(self, correct: bool, repeated: bool = False, format_correct: bool = True):
        self.correct = correct
        self.repeated = repeated
        self.format_correct = format_correct
        if not format_correct:
            self.correct = False

    def __bool__(self):
        return self.correct
