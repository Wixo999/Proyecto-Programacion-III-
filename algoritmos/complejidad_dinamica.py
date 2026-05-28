import time
import random
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)


# =========================================================
# MOCHILA PURA PARA MEDIR
# =========================================================

def _mochila_medir(items, capacidad):

    n = len(items)
    W = int(capacidad)

    tabla = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):

        peso  = items[i - 1]["peso"]
        valor = items[i - 1]["valor"]

        for w in range(W + 1):

            no_incluir = tabla[i - 1][w]

            if peso <= w:

                tabla[i][w] = max(no_incluir, valor + tabla[i - 1][w - peso])

            else:

                tabla[i][w] = no_incluir

    return tabla[n][W]


# =========================================================
# VENTANA COMPLEJIDAD PROG. DINAMICA  O(n*W)
# =========================================================

class VentanaComplejidadDinamica(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Complejidad Temporal — Prog. Dinámica O(n·W)")

        self.resize(750, 500)

        layout = QVBoxLayout()

        self.setLayout(layout)

        label = QLabel("Midiendo tiempos... por favor espere.")

        layout.addWidget(label)

        figura = self._generar_figura()

        canvas = FigureCanvas(figura)

        layout.addWidget(canvas)

        label.setText("Complejidad Teórica O(n·W)  vs  Práctica medida")

    # =====================================================
    # GENERAR FIGURA
    # =====================================================

    def _generar_figura(self):

        tamanios     = [10, 50, 100, 200, 400, 600, 800, 1000]
        capacidad_W  = 500
        repeticiones = 10
        tiempos      = []

        for n in tamanios:

            acumulado = 0

            for _ in range(repeticiones):

                items = [
                    {
                        "peso":  random.randint(1, 20),
                        "valor": random.randint(1, 3)
                    }
                    for _ in range(n)
                ]

                t0 = time.perf_counter()

                _mochila_medir(items, capacidad_W)

                acumulado += time.perf_counter() - t0

            tiempos.append(acumulado / repeticiones * 1_000_000)

        n_arr        = np.array(tamanios, dtype=float)
        t_arr        = np.array(tiempos,  dtype=float)
        teorica_base = n_arr * capacidad_W
        teorica      = (t_arr[0] / teorica_base[0]) * teorica_base

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(n_arr, teorica, "--", label="Teórica  O(n·W)",    linewidth=2)
        ax.plot(n_arr, t_arr,   "-o", label="Práctica (medida)",  linewidth=2)

        ax.set_title("Complejidad Temporal — Programación Dinámica")
        ax.set_xlabel("Cantidad de pedidos (n)   [W = 500 fijo]")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend()
        ax.grid(True)

        fig.tight_layout()

        return fig
