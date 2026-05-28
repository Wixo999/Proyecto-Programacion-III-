from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
)

from ui.panel_control import PanelControl

from ui.mapa_view import MapaView


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

class VentanaPrincipal(QMainWindow):

    def __init__(self):

        super().__init__()

        # =================================================
        # CONFIGURACION VENTANA
        # =================================================

        self.setWindowTitle(
            "Sistema de Rutas Óptimas — Cusco (Grafo OSMnx)"
        )

        self.resize(1400, 800)

        # =================================================
        # INICIALIZAR UI
        # =================================================

        self._inicializar_ui()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def _inicializar_ui(self):

        # =================================================
        # WIDGET CENTRAL
        # =================================================

        contenedor = QWidget()

        self.setCentralWidget(contenedor)

        # =================================================
        # LAYOUT PRINCIPAL
        # =================================================

        layout_principal = QHBoxLayout()

        contenedor.setLayout(layout_principal)

        # =================================================
        # MAPA  (se crea primero para pasarlo al panel)
        # =================================================

        self.mapa = MapaView()

        # =================================================
        # PANEL LATERAL
        # =================================================

        self.panel_control = PanelControl(mapa=self.mapa)

        # =================================================
        # AGREGAR ELEMENTOS (panel 1/5, mapa 4/5)
        # =================================================

        layout_principal.addWidget(self.panel_control, 1)

        layout_principal.addWidget(self.mapa, 4)
