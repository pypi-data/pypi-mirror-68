class DetectEnglish():

    def __init__(self, filepath):
        with open(filepath) as f:
            self.words = set(l.strip() for l in f)

    def english_score(self, text):
        return sum(1 for word in text if word.upper() in self.words) / len(text)
