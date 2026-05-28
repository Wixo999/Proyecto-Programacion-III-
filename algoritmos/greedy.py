from datos.repartidores import repartidores

from grafo.gestor_grafo import GestorGrafo


# =========================================================
# ALGORITMO GREEDY
#
# CASO DE USO:
# Asignacion de entregas rapidas o de emergencia.
#
# El repartidor mas cercano al pedido prioritario
# (medido por distancia real en calles, no euclidiana)
# es el asignado. O(n) sobre n repartidores.
#
# COMPLEJIDAD: O(n)
#   n = numero de repartidores
# =========================================================

def seleccionar_repartidor_greedy(

    nodo_pedido
):

    # =====================================================
    # OBTENER GESTOR DEL GRAFO
    # =====================================================

    gestor = GestorGrafo.obtener_instancia()

    # =====================================================
    # VARIABLES
    # =====================================================

    mejor_repartidor = None

    distancia_minima = float("inf")

    # =====================================================
    # RECORRER REPARTIDORES
    # =====================================================

    for repartidor in repartidores:

        # =================================================
        # DISTANCIA REAL POR CALLES
        # =================================================

        distancia_actual = gestor.distancia_real(

            repartidor.nodo_grafo,

            nodo_pedido
        )

        print(f"""

            Repartidor:  {repartidor.nombre}

            Distancia:   {round(distancia_actual, 1)} m

        """)

        # =================================================
        # GREEDY: ELEGIR EL MAS CERCANO
        # =================================================

        if distancia_actual < distancia_minima:

            distancia_minima = distancia_actual

            mejor_repartidor = repartidor

    # =====================================================
    # RETORNAR
    # =====================================================

    return mejor_repartidor, distancia_minima
