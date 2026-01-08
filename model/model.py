import networkx as nx
from geopy import distance
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.dao = DAO()
        self.stati_dict = {}

    def popola_dd(self):
        self.avvistamenti = self.dao.get_avvistamenti()
        anni = []
        forme = []
        for avvistamento in self.avvistamenti:
            if avvistamento.anno not in anni:
                anni.append(avvistamento.anno)
            if avvistamento.shape not in forme:
                forme.append(avvistamento.shape)
        return sorted(anni), forme


    def crea_grafo(self, anno, forma):
        self.G.clear()
        stati = self.dao.get_stati()

        for stato in stati:
            self.G.add_node(stato.id)
            self.stati_dict[stato.id] = stato
        stato_pesi_dict = {}
        for stato in stati:
            stato_pesi_dict[stato.id] = 0
            vicini = stato.neighbors
            for vicino in vicini:
                peso_stato = 0
                peso_vicino = 0
                for avvistamento in self.avvistamenti:
                    if avvistamento.state == stato.id and avvistamento.anno == anno and avvistamento.shape == forma:
                        peso_stato += 1
                    if avvistamento.state == vicino and avvistamento.anno == anno and avvistamento.shape == forma:
                        peso_vicino += 1
                if stato.id not in self.stati_dict[vicino].neighbors:
                    print("Neighbor non simmetrico:", stato.id, vicino)
                if peso_stato != 0:
                    self.G.add_edge(stato.id, vicino, weight = peso_stato + peso_vicino)
                    stato_pesi_dict[stato.id] += peso_stato + peso_vicino

        print(self.G)
        return self.G.number_of_nodes(), self.G.number_of_edges(), stato_pesi_dict

    def ricerca_percorso(self):
        self.percorso_ottimo = []
        self.distanza_ottima = 0
        for stato in self.G.nodes():
            self.ricorsione(nodo_corrente = stato, parziale = [stato], distanza_corrente = 0, peso_arco_corrente = 0)

        print(self.percorso_ottimo)
        print(self.distanza_ottima)
        return self.percorso_ottimo, self.distanza_ottima


    def ricorsione(self, nodo_corrente, parziale, distanza_corrente, peso_arco_corrente):

        if distanza_corrente > self.distanza_ottima:
            self.distanza_ottima = distanza_corrente
            self.percorso_ottimo = parziale.copy()

        vicini = self.G.neighbors(nodo_corrente)
        for vicino in vicini:
            if self.G[nodo_corrente][vicino]["weight"] > peso_arco_corrente:
                parziale.append(vicino)
                nuova_distanza = distanza_corrente + distance.geodesic((self.stati_dict[nodo_corrente].lat, self.stati_dict[nodo_corrente].lng), (self.stati_dict[vicino].lat, self.stati_dict[vicino].lng)) .km
                self.ricorsione(vicino, parziale, nuova_distanza, self.G[nodo_corrente][vicino]["weight"])
                parziale.pop()
