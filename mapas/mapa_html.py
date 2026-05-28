# =========================================================
# HTML BASE DEL MAPA
#
# Usa Leaflet con tiles CartoDB (efecto gris elegante).
# Los marcadores y rutas se inyectan dinamicamente desde
# mapa_view.py mediante runJavaScript().
#
# Limites exactos del area visible de Cusco:
#   SW: -13.565, -72.03
#   NE: -13.47,  -71.88
# =========================================================

html = """

<!DOCTYPE html>

<html>

<head>

    <!-- ================================================= -->
    <!-- LEAFLET CSS -->
    <!-- ================================================= -->

    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet/dist/leaflet.css"
    />

    <!-- ================================================= -->
    <!-- LEAFLET JS -->
    <!-- ================================================= -->

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

    <!-- ================================================= -->
    <!-- ESTILOS -->
    <!-- ================================================= -->

    <style>

        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }

        #map {
            width: 100%;
            height: 100%;
        }

        .leaflet-popup-content {
            font-size: 13px;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }

    </style>

</head>

<body>

    <!-- ================================================= -->
    <!-- CONTENEDOR DEL MAPA -->
    <!-- ================================================= -->

    <div id="map"></div>

    <!-- ================================================= -->
    <!-- JAVASCRIPT -->
    <!-- ================================================= -->

    <script>

        // =================================================
        // MAPA (CartoDB gris igual al notebook)
        // =================================================

        var map = L.map('map', {

            center: [-13.53195, -71.96746],
            zoom: 13,
            minZoom: 12,
            maxZoom: 17,
            maxBounds: [
                [-13.565, -72.03],
                [-13.47,  -71.88]
            ],
            maxBoundsViscosity: 1.0

        });

        // =================================================
        // CAPA BASE  (CartoDB positron = gris claro)
        // =================================================

        L.tileLayer(

            'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',

            {
                attribution: '© OpenStreetMap © CartoDB'
            }

        ).addTo(map);

        // =================================================
        // ICONO REPARTIDOR
        // =================================================

        var iconoRepartidor = L.icon({

            iconUrl:   'https://cdn-icons-png.flaticon.com/512/684/684908.png',
            iconSize:  [32, 32],
            iconAnchor:[16, 32]
        });

        // =================================================
        // CAPAS
        // =================================================

        var capaGrafo        = L.layerGroup().addTo(map);
        var capaRepartidores = L.layerGroup().addTo(map);
        var capaPedidos      = L.layerGroup().addTo(map);

        // =================================================
        // VARIABLES GLOBALES DE RUTAS Y CAPAS
        // =================================================

        window.rutaGreedy       = null;
        window.rutaBacktracking = null;
        window.capaCuadrantes   = null;
        window.capaMochila      = null;

        // =================================================
        // MARCADORES REPARTIDORES
        // =================================================

        {MARCADORES_REPARTIDORES}

        // =================================================
        // MARCADORES PEDIDOS
        // =================================================

        {MARCADORES_PEDIDOS}

    </script>

</body>

</html>

"""
