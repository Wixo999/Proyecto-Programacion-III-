import json

from PyQt5.QtWebEngineWidgets import QWebEngineView

from mapas.mapa_html     import html
from datos.repartidores  import repartidores
from datos.pedidos       import pedidos
from grafo.gestor_grafo  import GestorGrafo


# =========================================================
# MAPA VIEW
#
# Widget principal del mapa. Genera el HTML inicial con
# los marcadores y expone metodos para dibujar en el mapa
# cada algoritmo (Greedy, Backtracking, Divide, Mochila).
# =========================================================

class MapaView(QWebEngineView):

    def __init__(self):

        super().__init__()

        # =================================================
        # GENERAR HTML Y CARGAR
        # =================================================

        self._cargar_mapa()

    # =====================================================
    # CARGAR MAPA INICIAL
    # =====================================================

    def _cargar_mapa(self):

        # =================================================
        # GENERAR MARCADORES REPARTIDORES
        # =================================================

        marcadores_repartidores_js = ""

        for repartidor in repartidores:

            marcadores_repartidores_js += f"""

            L.marker(

                [{repartidor.latitud_actual}, {repartidor.longitud_actual}],

                {{ icon: iconoRepartidor }}

            )
            .addTo(capaRepartidores)
            .bindPopup(
                "<b>{repartidor.nombre}</b><br>" +
                "Vehiculo: {repartidor.vehiculo}<br>" +
                "Capacidad: {repartidor.capacidad_maxima} kg"
            );

            """

        # =================================================
        # GENERAR MARCADORES PEDIDOS
        #
        # Prioridad maxima -> amarillo / resto -> azul
        # =================================================

        prioridad_maxima = max(p.prioridad for p in pedidos)

        marcadores_pedidos_js = ""

        for pedido in pedidos:

            color = "yellow" if pedido.prioridad == prioridad_maxima else "steelblue"

            marcadores_pedidos_js += f"""

            L.circleMarker(

                [{pedido.latitud}, {pedido.longitud}],

                {{
                    color:       '{color}',
                    fillColor:   '{color}',
                    fillOpacity: 1,
                    radius:      8,
                    weight:      2
                }}

            )
            .addTo(capaPedidos)
            .bindPopup(
                "<b>Pedido #{pedido.id_pedido}</b><br>" +
                "Cliente: {pedido.cliente}<br>" +
                "Zona: {pedido.direccion}<br>" +
                "Prioridad: {pedido.prioridad}<br>" +
                "Peso: {pedido.peso} kg"
            );

            """

        # =================================================
        # INSERTAR EN HTML Y CARGAR
        # =================================================

        html_final = html.replace(
            "{MARCADORES_REPARTIDORES}",
            marcadores_repartidores_js
        )

        html_final = html_final.replace(
            "{MARCADORES_PEDIDOS}",
            marcadores_pedidos_js
        )

        self.setHtml(html_final)


    # =====================================================
    # DIBUJAR GRAFO EN EL MAPA
    #
    # Dibuja las calles (aristas) del grafo OSMnx
    # como polylines azules delgadas, igual al notebook.
    # =====================================================

    def dibujar_grafo(self):

        gestor = GestorGrafo.obtener_instancia()

        if not gestor.cargado:

            return

        # =================================================
        # OBTENER ARISTAS CON GEOMETRIA
        # =================================================

        import osmnx as ox

        edges = ox.graph_to_gdfs(gestor.grafo, nodes=False)

        # =================================================
        # CONSTRUIR ARRAY DE POLYLINES
        # =================================================

        lineas = []

        for _, row in edges.iterrows():

            if row.geometry.geom_type == "LineString":

                puntos = [
                    [lat, lon]
                    for lon, lat in row.geometry.coords
                ]

                lineas.append(puntos)

        # =================================================
        # JAVASCRIPT DINAMICO
        # =================================================

        lineas_json = json.dumps(lineas)

        js = f"""

        console.log("DIBUJANDO GRAFO...");

        capaGrafo.clearLayers();

        var lineas = {lineas_json};

        for (var i = 0; i < lineas.length; i++) {{

            L.polyline(
                lineas[i],
                {{
                    color:   '#4a90d9',
                    weight:  1,
                    opacity: 0.6
                }}
            ).addTo(capaGrafo);
        }}

        console.log("GRAFO DIBUJADO: " + lineas.length + " calles");

        """

        self.page().runJavaScript(js)


    # =====================================================
    # MOSTRAR RUTA GREEDY
    # =====================================================

    def mostrar_ruta_greedy(self, repartidor, pedido):

        gestor = GestorGrafo.obtener_instancia()

        # =================================================
        # OBTENER RUTA REAL POR CALLES
        # =================================================

        lista_nodos = gestor.ruta_real(

            repartidor.nodo_grafo,

            pedido.nodo_grafo
        )

        # =================================================
        # COORDENADAS DE LA RUTA
        # =================================================

        coordenadas = gestor.nodos_a_coordenadas(lista_nodos)

        coords_json = json.dumps(coordenadas)

        # =================================================
        # JAVASCRIPT DINAMICO
        # =================================================

        js = f"""

        console.log("DIBUJANDO RUTA GREEDY...");

        if (window.rutaGreedy) {{
            map.removeLayer(window.rutaGreedy);
        }}

        var puntos = {coords_json};

        window.rutaGreedy = L.polyline(
            puntos,
            {{
                color:   'blue',
                weight:  5,
                opacity: 0.9
            }}
        );

        window.rutaGreedy.addTo(map);

        window.rutaGreedy.bindPopup(
            "<b>Ruta Greedy</b><br>" +
            "Repartidor: {repartidor.nombre}<br>" +
            "Pedido: {pedido.cliente}<br>" +
            "Distancia real por calles"
        );

        map.fitBounds(window.rutaGreedy.getBounds(), {{ padding: [50, 50] }});

        console.log("RUTA GREEDY DIBUJADA");

        """

        self.page().runJavaScript(js)


    # =====================================================
    # MOSTRAR RUTA BACKTRACKING
    #
    # Dibuja la ruta optima (lista de pedidos) uniendo
    # cada par consecutivo por el camino real en calles.
    # =====================================================

    def mostrar_ruta_backtracking(self, ruta):

        gestor = GestorGrafo.obtener_instancia()

        # =================================================
        # CONSTRUIR SEGMENTOS REALES
        # =================================================

        todos_los_puntos = []

        for i in range(len(ruta) - 1):

            tramo = gestor.ruta_real(

                ruta[i].nodo_grafo,

                ruta[i + 1].nodo_grafo
            )

            todos_los_puntos += gestor.nodos_a_coordenadas(tramo)

        coords_json = json.dumps(todos_los_puntos)

        # =================================================
        # JAVASCRIPT DINAMICO
        # =================================================

        js = f"""

        console.log("DIBUJANDO RUTA BACKTRACKING...");

        if (window.rutaBacktracking) {{
            map.removeLayer(window.rutaBacktracking);
        }}

        window.rutaBacktracking = L.polyline(

            {coords_json},

            {{
                color:     'red',
                weight:    5,
                opacity:   0.9,
                dashArray: '12, 8'
            }}
        );

        window.rutaBacktracking.addTo(map);

        window.rutaBacktracking.bindPopup(
            "<b>Ruta Backtracking</b><br>" +
            "Ruta optima evitando sectores cerrados"
        );

        map.fitBounds(window.rutaBacktracking.getBounds(), {{ padding: [50, 50] }});

        console.log("RUTA BACKTRACKING DIBUJADA");

        """

        self.page().runJavaScript(js)


    # =====================================================
    # MOSTRAR CUADRANTES (DIVIDE Y VENCERAS)
    # =====================================================

    def mostrar_cuadrantes(self, centro_lat, centro_lon, cuadrantes):

        todas_lat = [
            p.latitud
            for k in cuadrantes
            for p in cuadrantes[k]
        ]

        todas_lon = [
            p.longitud
            for k in cuadrantes
            for p in cuadrantes[k]
        ]

        if not todas_lat:

            return

        margen = 0.005

        min_lat = min(todas_lat) - margen
        max_lat = max(todas_lat) + margen
        min_lon = min(todas_lon) - margen
        max_lon = max(todas_lon) + margen

        # =================================================
        # JAVASCRIPT DINAMICO
        # =================================================

        js = f"""

        console.log("DIBUJANDO CUADRANTES...");

        if (window.capaCuadrantes) {{
            map.removeLayer(window.capaCuadrantes);
        }}

        window.capaCuadrantes = L.layerGroup();

        // Cuadrante NO (rojo)
        L.rectangle(
            [[{centro_lat}, {min_lon}], [{max_lat}, {centro_lon}]],
            {{ color: '#e74c3c', weight: 2, fillOpacity: 0.12 }}
        )
        .bindPopup("<b>Cuadrante NO</b><br>{len(cuadrantes['NO'])} pedidos")
        .addTo(window.capaCuadrantes);

        // Cuadrante NE (azul)
        L.rectangle(
            [[{centro_lat}, {centro_lon}], [{max_lat}, {max_lon}]],
            {{ color: '#3498db', weight: 2, fillOpacity: 0.12 }}
        )
        .bindPopup("<b>Cuadrante NE</b><br>{len(cuadrantes['NE'])} pedidos")
        .addTo(window.capaCuadrantes);

        // Cuadrante SO (verde)
        L.rectangle(
            [[{min_lat}, {min_lon}], [{centro_lat}, {centro_lon}]],
            {{ color: '#2ecc71', weight: 2, fillOpacity: 0.12 }}
        )
        .bindPopup("<b>Cuadrante SO</b><br>{len(cuadrantes['SO'])} pedidos")
        .addTo(window.capaCuadrantes);

        // Cuadrante SE (naranja)
        L.rectangle(
            [[{min_lat}, {centro_lon}], [{centro_lat}, {max_lon}]],
            {{ color: '#f39c12', weight: 2, fillOpacity: 0.12 }}
        )
        .bindPopup("<b>Cuadrante SE</b><br>{len(cuadrantes['SE'])} pedidos")
        .addTo(window.capaCuadrantes);

        // Centro
        L.circleMarker(
            [{centro_lat}, {centro_lon}],
            {{
                color: 'black', fillColor: 'white',
                fillOpacity: 1, radius: 7, weight: 2
            }}
        )
        .bindPopup("<b>Centro de Cusco</b>")
        .addTo(window.capaCuadrantes);

        window.capaCuadrantes.addTo(map);

        console.log("CUADRANTES DIBUJADOS");

        """

        self.page().runJavaScript(js)


    # =====================================================
    # MOSTRAR MOCHILA (PROGRAMACION DINAMICA)
    # =====================================================

    def mostrar_mochila(self, seleccionados):

        marcadores_js = ""

        for pedido in seleccionados:

            marcadores_js += f"""

            L.circleMarker(

                [{pedido.latitud}, {pedido.longitud}],

                {{
                    color:       'green',
                    fillColor:   'lime',
                    fillOpacity: 1,
                    radius:      14,
                    weight:      4
                }}
            )
            .addTo(window.capaMochila)
            .bindPopup(
                "<b>Cargado en vehiculo</b><br>" +
                "Pedido #{pedido.id_pedido}<br>" +
                "Cliente: {pedido.cliente}<br>" +
                "Prioridad: {pedido.prioridad}<br>" +
                "Peso: {pedido.peso} kg"
            );

            """

        js = f"""

        console.log("DIBUJANDO MOCHILA...");

        if (window.capaMochila) {{
            map.removeLayer(window.capaMochila);
        }}

        window.capaMochila = L.layerGroup();

        {marcadores_js}

        window.capaMochila.addTo(map);

        console.log("MOCHILA DIBUJADA");

        """

        self.page().runJavaScript(js)
