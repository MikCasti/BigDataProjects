class Episodio:
    def __init__(self, stagione, episodio_numero):
        self.stagione = stagione
        self.episodio_numero = episodio_numero
        self.script = []
 
    def aggiungi_dialoghi(self, personaggio, battute):
        self.script.append({
            "nome_personaggio": personaggio,
            "battute": battute
        })
 
    def contiene_dialoghi(self):
        return bool(self.script)
