import csv

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base
        self.disponibile=True
        self.espositore=None

    def prezzo_finale(self):
        return self.prezzo_base

    def __str__(self):
        stato="Disponibile" if self.disponibile else f"Affittato a {self.espositore.nome} {self.espositore.cognome}"
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - {self.prezzo_finale():.2f}€ - {stato}"

    def __repr__(self):
        return f"Stand ('{self.codice}', {self.superficie}, {self.padiglione}, {self.prezzo_base})"

    def __eq__(self, other):
        if not isinstance(other, Stand):
            return False
        return self.codice == other.codice

    def  __lt__(self, other):
        return  self.prezzo_finale() < other.prezzo_finale()

class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese_extra=prese_extra


    def prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 * self.prese_extra)

    def __str__(self):
        stato="Disponibile" if self.disponibile else f"Affittato a {self.espositore.nome} {self.espositore.cognome}"
        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.prezzo_finale():.2f}€ - Prese aggiuntive: {self.prese_extra} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione=posizione

    def prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato="Disponibile" if self.disponibile else f"Affittato {self.espositore.nome} {self.espositore.cognome}"
        return f"{self.codice}: Premium | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale():.2f}€ - Posizione: {self.posizione} - {stato}"

class Espositore:
    def __init__(self,codice, nome, cognome):
        self.codice=codice
        self.nome=nome
        self.cognome=cognome
        self.stand=None

    def __str__(self):
        stato=f"Stand {self.stand.codice}" if self.stand is not None else ""
        return f"{self.codice} - {self.nome} {self.cognome} | {stato}"

    def __repr__(self):
        return f"Espositore ('{self.codice}', {self.nome}, {self.cognome})"

    def __eq__(self, other):
        if not isinstance(other, Espositore):
            return False
        return self.codice == other.codice


class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.stands=[]
        self.espositori=[]

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self,valore):
        if not valore or not isinstance(valore, str):
            raise ValueError("Nome non valido")
        self._nome = valore


    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        with open(file_path, "r", newline="") as f:
            reader=csv.reader(f)
            for riga in reader:
                if riga[0].startswith("ST"):
                    codice=riga[0]
                    superficie=int(riga[1])
                    padiglione=riga[2]
                    prezzo=float(riga[3])

                    if len(riga)==5:
                        #Controllo distinsione tipologia Stand
                        try:
                            prese=int(riga[4])
                            # è numerico -> StandPreseExtra
                            stand=StandPreseExtra(codice, superficie, padiglione, prezzo, prese)

                        except ValueError:
                            posizione=riga[4]
                            #è testuale -> StandPremium
                            stand = StandPremium(codice, superficie, padiglione, prezzo, posizione)

                    else:
                        stand=Stand(codice, superficie, padiglione, prezzo)

                    self.stands.append(stand)

                elif riga[0].startswith("ES"):
                    espositore=Espositore(riga[0], riga[1], riga[2])
                    self.espositori.append(espositore)


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand_trovato=None
        for stand in self.stands:
            if stand.codice == codice_stand:
                stand_trovato=stand
                break

        if stand_trovato is None:
            raise Exception("Stand non trovato")

        if not stand_trovato.disponibile:
            raise Exception("Stand già occupato")

        espositore_trovato=None

        for espositore in self.espositori:
            if espositore.codice == codice_espositore:
                espositore_trovato=espositore
                break

        if espositore_trovato is None:
            raise Exception("Espositore non trovato")

        if espositore_trovato.stand is not None:
            raise Exception("Espositore già assegnato")

        stand_trovato.espositore = espositore_trovato
        stand_trovato.disponibile = False
        espositore_trovato.stand = stand_trovato


    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori:
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stands)





