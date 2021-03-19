from toflit import Toflit
from portic import Portic

class Api():
    """
        Retourne un ensemble de méthodes pour requêter les bases toflit et portic
        - pour en savoir plus sur les endpoints toflit : help(client.toflit)
        - pour en savoir plus sur les endpoints portic : help(client.portic)
    """
    def __init__(self):
        self.toflit = Toflit()
        self.portic = Portic()
