import flet as ft
from geopy import distance


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO
        anni, forme = self._model.popola_dd()
        for anno in anni:
            self._view.dd_year.options.append(ft.dropdown.Option(anno))
        for forma in forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(forma))

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        nodi, archi, stato_pesi_dict = self._model.crea_grafo(int(self._view.dd_year.value), self._view.dd_shape.value)
        self._view.lista_visualizzazione_1.clean()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di Vertici:{nodi}, Numero di archi:{archi}"))
        for stato in stato_pesi_dict:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {stato.upper()}, somma pesi su archi: {stato_pesi_dict[stato]}"))
        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

        percorso, distanza_totale = self._model.ricerca_percorso()
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Peso cammino massimo: {distanza_totale}"))
        for i in range(0, len(percorso)-1):
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{percorso[i].upper()} --> {percorso[i+1].upper()} weight {self._model.G[percorso[i]][percorso[i+1]]["weight"]}, distance {distance.geodesic((self._model.stati_dict[percorso[i]].lat, self._model.stati_dict[percorso[i]].lng), (self._model.stati_dict[percorso[i+1]].lat, self._model.stati_dict[percorso[i+1]].lng)) .km}"))
        self._view.update()
