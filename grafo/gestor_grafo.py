import osmnx as ox
import networkx as nx

from datos.pedidos     import pedidos
from datos.repartidores import repartidores


# =========================================================
# CONFIGURACION DEL GRAFO
# =========================================================

CENTRO_CUSCO  = (-13.53195, -71.96746)

RADIO_METROS  = 3000

TIPO_RED      = "drive"


# =========================================================
# GESTOR DEL GRAFO
#
# Singleton: descarga el grafo una sola vez y expone
# metodos utiles para los algoritmos.
# =========================================================

class GestorGrafo:

    # =====================================================
    # INSTANCIA UNICA
    # =====================================================

    _instancia = None

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self):

        # =================================================
        # GRAFO OSMNX
        # =================================================

        self.grafo = None

        # =================================================
        # INDICADOR DE CARGA
        # =================================================

        self.cargado = False

    # =====================================================
    # OBTENER INSTANCIA UNICA (SINGLETON)
    # =====================================================

    @classmethod
    def obtener_instancia(cls):

        if cls._instancia is None:

            cls._instancia = GestorGrafo()

        return cls._instancia

    # =====================================================
    # DESCARGAR GRAFO
    #
    # Descarga el grafo de calles de Cusco desde OSM.
    # Solo se ejecuta una vez.
    # =====================================================

    def descargar(self):

        if self.cargado:

            return

        print("======================================")
        print("DESCARGANDO GRAFO DE CUSCO...")
        print("======================================")

        # =================================================
        # DESCARGAR GRAFO
        # =================================================

        self.grafo = ox.graph_from_point(

            CENTRO_CUSCO,

            dist=RADIO_METROS,

            network_type=TIPO_RED
        )

        # =================================================
        # AGREGAR VELOCIDADES Y TIEMPOS DE VIAJE
        # =================================================

        self.grafo = ox.add_edge_speeds(self.grafo)

        self.grafo = ox.add_edge_travel_times(self.grafo)

        # =================================================
        # ASIGNAR NODOS A PEDIDOS Y REPARTIDORES
        # =================================================

        self._asignar_nodos_pedidos()

        self._asignar_nodos_repartidores()

        self.cargado = True

        print("GRAFO LISTO")
        print(f"  Nodos:  {self.grafo.number_of_nodes()}")
        print(f"  Aristas:{self.grafo.number_of_edges()}")

    # =====================================================
    # ASIGNAR NODO DEL GRAFO A CADA PEDIDO
    # =====================================================

    def _asignar_nodos_pedidos(self):

        for pedido in pedidos:

            nodo = ox.distance.nearest_nodes(

                self.grafo,

                pedido.longitud,
                pedido.latitud
            )

            pedido.nodo_grafo = nodo

    # =====================================================
    # ASIGNAR NODO DEL GRAFO A CADA REPARTIDOR
    # =====================================================

    def _asignar_nodos_repartidores(self):

        for repartidor in repartidores:

            nodo = ox.distance.nearest_nodes(

                self.grafo,

                repartidor.longitud_actual,
                repartidor.latitud_actual
            )

            repartidor.nodo_grafo = nodo

    # =====================================================
    # OBTENER NODO MAS CERCANO A COORDENADAS
    # =====================================================

    def nodo_cercano(self, latitud, longitud):

        return ox.distance.nearest_nodes(

            self.grafo,

            longitud,
            latitud
        )

    # =====================================================
    # DISTANCIA REAL POR CALLES (METROS)
    #
    # Usa Dijkstra internamente (NetworkX).
    # Retorna float("inf") si no hay camino.
    # =====================================================

    def distancia_real(self, nodo_origen, nodo_destino):

        try:

            return nx.shortest_path_length(

                self.grafo,

                nodo_origen,
                nodo_destino,

                weight="length"
            )

        except nx.NetworkXNoPath:

            return float("inf")

        except nx.NodeNotFound:

            return float("inf")

    # =====================================================
    # RUTA REAL POR CALLES
    #
    # Devuelve la lista de nodos del camino mas corto.
    # Retorna [] si no hay camino.
    # =====================================================

    def ruta_real(self, nodo_origen, nodo_destino):

        try:

            return nx.shortest_path(

                self.grafo,

                nodo_origen,
                nodo_destino,

                weight="length"
            )

        except nx.NetworkXNoPath:

            return []

        except nx.NodeNotFound:

            return []

    # =====================================================
    # NODOS VECINOS DIRECTOS
    #
    # Para el backtracking: expansores del nodo actual.
    # =====================================================

    def vecinos(self, nodo):

        return list(self.grafo.neighbors(nodo))

    # =====================================================
    # COORDENADAS DE UN NODO
    # =====================================================

    def coordenadas_nodo(self, nodo):

        datos = self.grafo.nodes[nodo]

        return datos["y"], datos["x"]

    # =====================================================
    # NODOS → COORDENADAS  (para dibujar en Leaflet)
    #
    # Convierte lista de nodos en lista de [lat, lon].
    # =====================================================

    def nodos_a_coordenadas(self, lista_nodos):

        coords = []

        for nodo in lista_nodos:

            lat, lon = self.coordenadas_nodo(nodo)

            coords.append([lat, lon])

        return coords
