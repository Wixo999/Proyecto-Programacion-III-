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
# PAR MAS CERCANO PURO PARA MEDIR (sin OSMnx)
# =========================================================

def _distancia(a, b):

    return math.sqrt(
        (a["lat"] - b["lat"]) ** 2
        + (a["lon"] - b["lon"]) ** 2
    )


def _par_mas_cercano_medir(puntos):

    def fuerza_bruta(grupo):

        mejor = float("inf")

        for i in range(len(grupo)):

            for j in range(i + 1, len(grupo)):

                mejor = min(mejor, _distancia(grupo[i], grupo[j]))

        return mejor

    def recursivo(grupo):

        if len(grupo) <= 3:

            return fuerza_bruta(grupo)

        medio = len(grupo) // 2

        mejor = min(
            recursivo(grupo[:medio]),
            recursivo(grupo[medio:])
        )

        lon_div = grupo[medio]["lon"]

        franja = sorted(
            [p for p in grupo if abs(p["lon"] - lon_div) < mejor],
            key=lambda p: p["lat"]
        )

        for i in range(len(franja)):

            for j in range(i + 1, len(franja)):

                if franja[j]["lat"] - franja[i]["lat"] >= mejor:

                    break

                mejor = min(mejor, _distancia(franja[i], franja[j]))

        return mejor

    puntos_ord = sorted(puntos, key=lambda p: p["lon"])

    return recursivo(puntos_ord)


# =========================================================
# VENTANA COMPLEJIDAD DIVIDE Y VENCERAS  O(n log n)
# =========================================================

class VentanaComplejidadDivide(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Complejidad Temporal — Divide y Vencerás O(n log n)")

        self.resize(750, 500)

        layout = QVBoxLayout()

        self.setLayout(layout)

        label = QLabel("Midiendo tiempos... por favor espere.")

        layout.addWidget(label)

        figura = self._generar_figura()

        canvas = FigureCanvas(figura)

        layout.addWidget(canvas)

        label.setText("Complejidad Teórica O(n log n)  vs  Práctica medida")

    # =====================================================
    # GENERAR FIGURA
    # =====================================================

    def _generar_figura(self):

        tamanios     = [10, 100, 500, 1000, 3000, 5000, 8000, 10000]
        repeticiones = 20
        tiempos      = []

        for n in tamanios:

            acumulado = 0

            for _ in range(repeticiones):

                puntos = [
                    {
                        "lat": random.uniform(-13.60, -13.48),
                        "lon": random.uniform(-72.05, -71.90)
                    }
                    for _ in range(n)
                ]

                t0 = time.perf_counter()

                _par_mas_cercano_medir(puntos)

                acumulado += time.perf_counter() - t0

            tiempos.append(acumulado / repeticiones * 1_000_000)

        n_arr   = np.array(tamanios, dtype=float)
        t_arr   = np.array(tiempos,  dtype=float)
        n_log_n = n_arr * np.log2(n_arr)
        teorica = (t_arr[0] / n_log_n[0]) * n_log_n

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(n_arr, teorica, "--", label="Teórica  O(n log n)", linewidth=2)
        ax.plot(n_arr, t_arr,   "-o", label="Práctica (medida)",   linewidth=2)

        ax.set_title("Complejidad Temporal — Divide y Vencerás")
        ax.set_xlabel("Cantidad de pedidos (n)")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend()
        ax.grid(True)

        fig.tight_layout()

        return fig
