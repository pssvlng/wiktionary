from BaseWord import BaseWord

class ContextWord(BaseWord):           
    def __init__(self):
        super().__init__()                
        self.lemma = ''
        self.whitespace = ''
        self.isPropNoun = False
        self.lang = 'en'
        self.linked_data = []
        
