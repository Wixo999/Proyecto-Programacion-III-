from datos.pedidos import pedidos


# =========================================================
# PROGRAMACION DINAMICA
#
# CASO DE USO:
# Optimizacion estricta de recursos.
#
# Resuelve el Problema de la Mochila 0/1 (Knapsack)
# para cargar el vehiculo del repartidor maximizando
# el VALOR (prioridad) de los pedidos sin superar el
# PESO maximo (capacidad del vehiculo).
#
# COMPLEJIDAD: O(n * W)
#   n = cantidad de pedidos
#   W = capacidad maxima del repartidor (entero)
# =========================================================

def resolver_mochila(

    capacidad,

    lista_pedidos=None
):

    # =====================================================
    # LISTA POR DEFECTO
    # =====================================================

    if lista_pedidos is None:

        lista_pedidos = pedidos

    # =====================================================
    # PARAMETROS
    # =====================================================

    n = len(lista_pedidos)

    W = int(capacidad)

    # =====================================================
    # CONSTRUIR TABLA DP
    #
    # tabla[i][w] = mejor valor usando los primeros i
    #               pedidos con capacidad w disponible.
    # =====================================================

    tabla = [
        [0] * (W + 1)
        for _ in range(n + 1)
    ]

    # =====================================================
    # LLENAR TABLA
    # =====================================================

    for i in range(1, n + 1):

        pedido_actual = lista_pedidos[i - 1]

        peso_pedido   = int(pedido_actual.peso)

        valor_pedido  = pedido_actual.prioridad

        for w in range(W + 1):

            # =============================================
            # OPCION 1: NO INCLUIR
            # =============================================

            no_incluir = tabla[i - 1][w]

            # =============================================
            # OPCION 2: INCLUIR (si el peso lo permite)
            # =============================================

            if peso_pedido <= w:

                incluir = (
                    valor_pedido
                    + tabla[i - 1][w - peso_pedido]
                )

                tabla[i][w] = max(no_incluir, incluir)

            else:

                tabla[i][w] = no_incluir

    # =====================================================
    # RECONSTRUIR SOLUCION
    #
    # Recorre la tabla hacia atras para saber cuales
    # pedidos fueron incluidos.
    # =====================================================

    pedidos_seleccionados = []

    w = W

    for i in range(n, 0, -1):

        if tabla[i][w] != tabla[i - 1][w]:

            pedido_incluido = lista_pedidos[i - 1]

            pedidos_seleccionados.append(pedido_incluido)

            w -= int(pedido_incluido.peso)

    # =====================================================
    # TOTALES
    # =====================================================

    peso_total  = sum(p.peso      for p in pedidos_seleccionados)

    valor_total = tabla[n][W]

    # =====================================================
    # RETORNAR
    # =====================================================

    return pedidos_seleccionados, valor_total, peso_total
