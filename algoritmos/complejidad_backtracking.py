import time
import random
import math
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
# BACKTRACKING PURO PARA MEDIR (sin OSMnx)
# =========================================================

def _calcular_distancia(a, b):

    return math.sqrt(
        (a["lat"] - b["lat"]) ** 2
        + (a["lon"] - b["lon"]) ** 2
    )


def _backtracking_medir(origen, destino, intermedios):

    rutas = []

    def backtrack(ruta_actual, restantes):

        secuencia = [origen] + ruta_actual + [destino]

        distancia = sum(
            _calcular_distancia(secuencia[i], secuencia[i + 1])
            for i in range(len(secuencia) - 1)
        )

        rutas.append(distancia)

        for i in range(len(restantes)):

            backtrack(
                ruta_actual + [restantes[i]],
                restantes[:i] + restantes[i + 1:]
            )

    backtrack([], intermedios)

    return rutas


# =========================================================
# VENTANA COMPLEJIDAD BACKTRACKING  O(n!)
# =========================================================

class VentanaComplejidadBacktracking(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Complejidad Temporal — Backtracking O(n!)")

        self.resize(750, 500)

        layout = QVBoxLayout()

        self.setLayout(layout)

        label = QLabel("Midiendo tiempos... por favor espere.")

        layout.addWidget(label)

        figura = self._generar_figura()

        canvas = FigureCanvas(figura)

        layout.addWidget(canvas)

        label.setText("Complejidad Teórica O(n!)  vs  Práctica medida")

    # =====================================================
    # GENERAR FIGURA
    # =====================================================

    def _generar_figura(self):

        tamanios     = [1, 2, 3, 4, 5, 6, 7, 8]
        repeticiones = 5
        tiempos      = []

        for n in tamanios:

            origen  = {"lat": -13.52, "lon": -71.97}
            destino = {"lat": -13.53, "lon": -71.96}

            acumulado = 0

            for _ in range(repeticiones):

                intermedios = [
                    {
                        "lat": random.uniform(-13.60, -13.48),
                        "lon": random.uniform(-72.05, -71.90)
                    }
                    for _ in range(n)
                ]

                t0 = time.perf_counter()

                _backtracking_medir(origen, destino, intermedios)

                acumulado += time.perf_counter() - t0

            tiempos.append(acumulado / repeticiones * 1_000_000)

        n_arr       = np.array(tamanios, dtype=float)
        t_arr       = np.array(tiempos,  dtype=float)
        factoriales = np.array([math.factorial(int(n)) for n in n_arr], dtype=float)
        teorica     = (t_arr[0] / factoriales[0]) * factoriales

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(n_arr, teorica, "--", label="Teórica  O(n!)",     linewidth=2)
        ax.plot(n_arr, t_arr,   "-o", label="Práctica (medida)",  linewidth=2)

        ax.set_title("Complejidad Temporal — Backtracking")
        ax.set_xlabel("Pedidos intermedios (n)")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend()
        ax.grid(True)

        fig.tight_layout()

        return fig
