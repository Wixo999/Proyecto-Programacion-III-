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
# GREEDY PURO PARA MEDIR (sin OSMnx, usa euclidiana)
# =========================================================

def _greedy_medir(repartidores, lat_pedido, lon_pedido):

    mejor   = None
    minimo  = float("inf")

    for r in repartidores:

        d = math.sqrt(
            (r["lat"] - lat_pedido) ** 2
            + (r["lon"] - lon_pedido) ** 2
        )

        if d < minimo:
            minimo = d
            mejor  = r

    return mejor, minimo


# =========================================================
# VENTANA COMPLEJIDAD GREEDY  O(n)
# =========================================================

class VentanaComplejidadGreedy(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Complejidad Temporal — Greedy O(n)")

        self.resize(750, 500)

        layout = QVBoxLayout()

        self.setLayout(layout)

        label = QLabel("Midiendo tiempos... por favor espere.")

        layout.addWidget(label)

        figura = self._generar_figura()

        canvas = FigureCanvas(figura)

        layout.addWidget(canvas)

        label.setText("Complejidad Teórica O(n)  vs  Práctica medida")

    # =====================================================
    # GENERAR FIGURA
    # =====================================================

    def _generar_figura(self):

        tamanios     = [10, 100, 500, 1000, 3000, 5000, 8000, 10000]
        repeticiones = 50
        tiempos      = []

        for n in tamanios:

            repartidores = [
                {
                    "lat": random.uniform(-13.60, -13.48),
                    "lon": random.uniform(-72.05, -71.90)
                }
                for _ in range(n)
            ]

            acumulado = 0

            for _ in range(repeticiones):

                lat = random.uniform(-13.60, -13.48)
                lon = random.uniform(-72.05, -71.90)

                t0 = time.perf_counter()

                _greedy_medir(repartidores, lat, lon)

                acumulado += time.perf_counter() - t0

            tiempos.append(acumulado / repeticiones * 1_000_000)

        n_arr   = np.array(tamanios, dtype=float)
        t_arr   = np.array(tiempos,  dtype=float)
        teorica = (t_arr[0] / n_arr[0]) * n_arr

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(n_arr, teorica, "--", label="Teórica  O(n)",        linewidth=2)
        ax.plot(n_arr, t_arr,   "-o", label="Práctica (medida)",    linewidth=2)

        ax.set_title("Complejidad Temporal — Greedy")
        ax.set_xlabel("Cantidad de repartidores (n)")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend()
        ax.grid(True)

        fig.tight_layout()

        return fig
