from datos.pedidos import pedidos

from grafo.gestor_grafo import GestorGrafo


# =========================================================
# DIVIDE Y VENCERAS
#
# CASO DE USO:
# Segmentacion de la ciudad en cuadrantes.
#
# Divide el mapa de Cusco en 4 zonas geograficas a
# partir del centro de los pedidos. Dentro de cada zona
# se aplica el algoritmo del PAR MAS CERCANO (D y V)
# usando distancias reales por calles.
#
# COMPLEJIDAD:
#   Segmentar:      O(n)
#   Par mas cercano: O(n log n)
# =========================================================


# =========================================================
# PASO 1 - SEGMENTAR CIUDAD EN CUADRANTES
# =========================================================

def segmentar_ciudad(lista_pedidos=None):

    if lista_pedidos is None:

        lista_pedidos = pedidos

    # =====================================================
    # CALCULAR CENTRO
    # =====================================================

    suma_lat = sum(p.latitud  for p in lista_pedidos)

    suma_lon = sum(p.longitud for p in lista_pedidos)

    centro_lat = suma_lat / len(lista_pedidos)

    centro_lon = suma_lon / len(lista_pedidos)

    # =====================================================
    # CLASIFICAR EN CUADRANTES
    #
    # NO = Nor-Oeste
    # NE = Nor-Este
    # SO = Sur-Oeste
    # SE = Sur-Este
    # =====================================================

    cuadrantes = { "NO": [], "NE": [], "SO": [], "SE": [] }

    for pedido in lista_pedidos:

        norte = pedido.latitud  >= centro_lat

        este  = pedido.longitud >= centro_lon

        if   norte and not este:  cuadrantes["NO"].append(pedido)
        elif norte and     este:  cuadrantes["NE"].append(pedido)
        elif not norte and not este: cuadrantes["SO"].append(pedido)
        else:                     cuadrantes["SE"].append(pedido)

    return centro_lat, centro_lon, cuadrantes


# =========================================================
# PASO 2 - PAR MAS CERCANO (DIVIDE Y VENCERAS)
#
# Dentro de un cuadrante, encuentra el par de pedidos
# mas cercanos usando distancia real por calles.
#
# Por el costo de Dijkstra, se usa distancia euclidiana
# en la recursion y solo se valida con distancia real
# el par final ganador.
# =========================================================

def par_mas_cercano(lista_pedidos):

    gestor = GestorGrafo.obtener_instancia()

    # =====================================================
    # MENOS DE 2 PUNTOS
    # =====================================================

    if len(lista_pedidos) < 2:

        return None, None, float("inf")

    # =====================================================
    # DISTANCIA EUCLIDIANA (para la recursion interna)
    # =====================================================

    def distancia_euclidiana(a, b):

        return (
            (a.latitud  - b.latitud)  ** 2
            + (a.longitud - b.longitud) ** 2
        ) ** 0.5

    # =====================================================
    # FUERZA BRUTA (grupos pequenos <= 3 puntos)
    # =====================================================

    def fuerza_bruta(grupo):

        mejor_a = None
        mejor_b = None
        mejor_d = float("inf")

        for i in range(len(grupo)):

            for j in range(i + 1, len(grupo)):

                d = distancia_euclidiana(grupo[i], grupo[j])

                if d < mejor_d:

                    mejor_d = d
                    mejor_a = grupo[i]
                    mejor_b = grupo[j]

        return mejor_a, mejor_b, mejor_d

    # =====================================================
    # RECURSION  (DIVIDE Y VENCERAS)
    # =====================================================

    def recursivo(grupo):

        # =================================================
        # CASO BASE
        # =================================================

        if len(grupo) <= 3:

            return fuerza_bruta(grupo)

        # =================================================
        # DIVIDIR
        # =================================================

        medio     = len(grupo) // 2

        izquierda = grupo[:medio]

        derecha   = grupo[medio:]

        # =================================================
        # VENCER
        # =================================================

        a_izq, b_izq, d_izq = recursivo(izquierda)

        a_der, b_der, d_der = recursivo(derecha)

        # =================================================
        # COMBINAR
        # =================================================

        if d_izq < d_der:

            mejor_a, mejor_b, mejor_d = a_izq, b_izq, d_izq

        else:

            mejor_a, mejor_b, mejor_d = a_der, b_der, d_der

        # =================================================
        # FRANJA CENTRAL
        # =================================================

        lon_division = grupo[medio].longitud

        franja = [
            p for p in grupo
            if abs(p.longitud - lon_division) < mejor_d
        ]

        franja.sort(key=lambda p: p.latitud)

        for i in range(len(franja)):

            for j in range(i + 1, len(franja)):

                if (franja[j].latitud - franja[i].latitud) >= mejor_d:

                    break

                d = distancia_euclidiana(franja[i], franja[j])

                if d < mejor_d:

                    mejor_d = d
                    mejor_a = franja[i]
                    mejor_b = franja[j]

        return mejor_a, mejor_b, mejor_d

    # =====================================================
    # ORDENAR POR LONGITUD Y EJECUTAR
    # =====================================================

    puntos = sorted(lista_pedidos, key=lambda p: p.longitud)

    pedido_a, pedido_b, _ = recursivo(puntos)

    # =====================================================
    # DISTANCIA REAL FINAL (por calles reales de Cusco)
    # =====================================================

    if pedido_a is not None and pedido_b is not None:

        distancia_real = gestor.distancia_real(

            pedido_a.nodo_grafo,

            pedido_b.nodo_grafo
        )

    else:

        distancia_real = float("inf")

    return pedido_a, pedido_b, distancia_real
