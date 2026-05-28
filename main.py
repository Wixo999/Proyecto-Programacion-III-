import sys

from PyQt5.QtWidgets import QApplication

from ui.ventana_principal import VentanaPrincipal


# =========================================================
# INICIAR APLICACION
# =========================================================

app = QApplication(sys.argv)

# =========================================================
# CREAR VENTANA PRINCIPAL
# =========================================================

ventana = VentanaPrincipal()

# =========================================================
# MOSTRAR VENTANA
# =========================================================

ventana.show()

# =========================================================
# EJECUTAR APP
# =========================================================

sys.exit(app.exec_())
