import networkx as nx

from datos.pedidos import pedidos

from grafo.gestor_grafo import GestorGrafo


# =========================================================
# ALGORITMO BACKTRACKING
#
# CASO DE USO:
# Rutas con restricciones estrictas sobre el grafo real.
#
# Encuentra todas las rutas entre dos pedidos (origen y
# destino) que pasen por pedidos intermedios, evitando
# los nodos de sectores cerrados por mantenimiento,
# y selecciona al final la mas corta en metros reales.
#
# COMPLEJIDAD: O(n!)
#   n = cantidad de pedidos intermedios validos
# =========================================================

def buscar_rutas_backtracking(

    id_origen,
    id_destino,

    sectores_bloqueados=None,

    ids_permitidos=None
):

    # =====================================================
    # PREPARAR SECTORES BLOQUEADOS
    # =====================================================

    if sectores_bloqueados is None:

        sectores_bloqueados = []

    # =====================================================
    # OBTENER GESTOR
    # =====================================================

    gestor = GestorGrafo.obtener_instancia()

    # =====================================================
    # BUSCAR PEDIDO ORIGEN Y DESTINO
    # =====================================================

    pedido_origen  = None

    pedido_destino = None

    for pedido in pedidos:

        if pedido.id_pedido == id_origen:

            pedido_origen = pedido

        if pedido.id_pedido == id_destino:

            pedido_destino = pedido

    if pedido_origen is None or pedido_destino is None:

        return [], None

    # =====================================================
    # PEDIDOS INTERMEDIOS
    #
    # Excluir origen, destino, sectores bloqueados y
    # los que no esten en ids_permitidos (limite O(n!)).
    # =====================================================

    intermedios = []

    for pedido in pedidos:

        es_origen  = (pedido.id_pedido == id_origen)

        es_destino = (pedido.id_pedido == id_destino)

        bloqueado  = (pedido.direccion in sectores_bloqueados)

        if ids_permitidos is None:

            permitido = True

        else:

            permitido = (pedido.id_pedido in ids_permitidos)

        if (
            not es_origen
            and not es_destino
            and not bloqueado
            and permitido
        ):

            intermedios.append(pedido)

    # =====================================================
    # ACUMULADORES
    # =====================================================

    rutas_validas = []

    # =====================================================
    # FUNCION RECURSIVA (BACKTRACKING)
    # =====================================================

    def backtrack(ruta_actual, restantes):

        # =================================================
        # CONSTRUIR RUTA COMPLETA
        # =================================================

        secuencia = (
            [pedido_origen]
            + ruta_actual
            + [pedido_destino]
        )

        # =================================================
        # CALCULAR DISTANCIA REAL DE LA RUTA COMPLETA
        #
        # Suma las distancias reales por calles entre
        # cada par consecutivo de pedidos.
        # =================================================

        distancia_total = 0

        for i in range(len(secuencia) - 1):

            distancia_total += gestor.distancia_real(

                secuencia[i].nodo_grafo,

                secuencia[i + 1].nodo_grafo
            )

        # =================================================
        # GUARDAR RUTA VALIDA
        # =================================================

        rutas_validas.append(
            {
                "ruta":      secuencia,
                "distancia": distancia_total
            }
        )

        # =================================================
        # EXPANSION
        # =================================================

        for i in range(len(restantes)):

            # ---------------------------------------------
            # ELEGIR
            # ---------------------------------------------

            siguiente = restantes[i]

            nuevos_restantes = (
                restantes[:i]
                + restantes[i + 1:]
            )

            # ---------------------------------------------
            # EXPLORAR
            # ---------------------------------------------

            backtrack(

                ruta_actual + [siguiente],

                nuevos_restantes
            )

            # ---------------------------------------------
            # DESHACER (implicito al volver del recursivo)
            # ---------------------------------------------

    # =====================================================
    # LANZAR BACKTRACKING
    # =====================================================

    backtrack([], intermedios)

    # =====================================================
    # SELECCIONAR LA RUTA MAS CORTA
    # =====================================================

    mejor_ruta       = None

    distancia_minima = float("inf")

    for ruta in rutas_validas:

        if ruta["distancia"] < distancia_minima:

            distancia_minima = ruta["distancia"]

            mejor_ruta = ruta

    return rutas_validas, mejor_ruta
