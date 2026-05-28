from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QProgressDialog
)

from PyQt5.QtCore import Qt

from datos.pedidos import (
    Pedido,
    agregar_pedido,
    buscar_pedido,
    buscar_pedidos_por_sector,
    pedidos
)

from datos.repartidores import repartidores

from grafo.gestor_grafo import GestorGrafo

# =========================================================
# IMPORTAR ALGORITMOS
# =========================================================

from algoritmos.greedy import (
    seleccionar_repartidor_greedy
)

from algoritmos.backtracking import (
    buscar_rutas_backtracking
)

from algoritmos.divide_venceras import (
    segmentar_ciudad
)

from algoritmos.dinamica import (
    resolver_mochila
)

# =========================================================
# IMPORTAR VENTANAS DE COMPLEJIDAD
# =========================================================

from algoritmos.complejidad_greedy import (
    VentanaComplejidadGreedy
)

from algoritmos.complejidad_backtracking import (
    VentanaComplejidadBacktracking
)

from algoritmos.complejidad_divide import (
    VentanaComplejidadDivide
)

from algoritmos.complejidad_dinamica import (
    VentanaComplejidadDinamica
)


# =========================================================
# PANEL DE CONTROL
# =========================================================

class PanelControl(QWidget):

    def __init__(self, mapa=None):

        super().__init__()

        # =================================================
        # REFERENCIAS
        # =================================================

        self.mapa = mapa

        self.id_actual_pedido = len(pedidos) + 1

        # =================================================
        # LAYOUT PRINCIPAL
        # =================================================

        layout = QVBoxLayout()

        self.setLayout(layout)

        # =================================================
        # TITULO
        # =================================================

        titulo = QLabel("PANEL DE CONTROL")

        layout.addWidget(titulo)

        # =================================================
        # =================================================
        # SECCION GRAFO
        # =================================================
        # =================================================

        grafo_group = QGroupBox("GRAFO DE CALLES")

        grafo_layout = QVBoxLayout()

        grafo_group.setLayout(grafo_layout)

        btn_cargar_grafo = QPushButton("Cargar Grafo de Cusco")

        btn_mostrar_grafo = QPushButton("Mostrar Calles en Mapa")

        btn_cargar_grafo.clicked.connect(self.cargar_grafo)

        btn_mostrar_grafo.clicked.connect(self.mostrar_grafo)

        grafo_layout.addWidget(btn_cargar_grafo)

        grafo_layout.addWidget(btn_mostrar_grafo)

        layout.addWidget(grafo_group)

        # =================================================
        # =================================================
        # FORMULARIO PEDIDOS
        # =================================================
        # =================================================

        formulario_group = QGroupBox("REGISTRO DE PEDIDOS")

        formulario_layout = QFormLayout()

        formulario_group.setLayout(formulario_layout)

        # =================================================
        # CLIENTE
        # =================================================

        self.input_cliente = QLineEdit()

        formulario_layout.addRow("Cliente:", self.input_cliente)

        # =================================================
        # DIRECCION
        # =================================================

        self.input_direccion = QLineEdit()

        formulario_layout.addRow("Dirección:", self.input_direccion)

        # =================================================
        # LATITUD
        # =================================================

        self.input_latitud = QDoubleSpinBox()

        self.input_latitud.setDecimals(6)

        self.input_latitud.setRange(-90, 90)

        formulario_layout.addRow("Latitud:", self.input_latitud)

        # =================================================
        # LONGITUD
        # =================================================

        self.input_longitud = QDoubleSpinBox()

        self.input_longitud.setDecimals(6)

        self.input_longitud.setRange(-180, 180)

        formulario_layout.addRow("Longitud:", self.input_longitud)

        # =================================================
        # PRIORIDAD
        # =================================================

        self.input_prioridad = QComboBox()

        self.input_prioridad.addItem("Baja",    1)
        self.input_prioridad.addItem("Media",   2)
        self.input_prioridad.addItem("Urgente", 3)

        formulario_layout.addRow("Prioridad:", self.input_prioridad)

        # =================================================
        # PESO
        # =================================================

        self.input_peso = QDoubleSpinBox()

        self.input_peso.setRange(0, 1000)

        self.input_peso.setSuffix(" kg")

        formulario_layout.addRow("Peso:", self.input_peso)

        # =================================================
        # BOTON REGISTRAR
        # =================================================

        btn_registrar = QPushButton("Registrar Pedido")

        btn_registrar.clicked.connect(self.registrar_pedido)

        formulario_layout.addRow(btn_registrar)

        layout.addWidget(formulario_group)

        # =================================================
        # =================================================
        # SECCION BUSQUEDA
        # =================================================
        # =================================================

        busqueda_group = QGroupBox("BÚSQUEDA DE PEDIDOS")

        busqueda_layout = QFormLayout()

        busqueda_group.setLayout(busqueda_layout)

        # =================================================
        # CAMPO BUSQUEDA
        # =================================================

        self.input_busqueda = QLineEdit()

        self.input_busqueda.setPlaceholderText("ID o sector...")

        busqueda_layout.addRow("Buscar:", self.input_busqueda)

        # =================================================
        # TIPO DE BUSQUEDA
        # =================================================

        self.combo_busqueda = QComboBox()

        self.combo_busqueda.addItem("Por ID",     "id")
        self.combo_busqueda.addItem("Por Sector", "sector")

        busqueda_layout.addRow("Tipo:", self.combo_busqueda)

        # =================================================
        # COMBO ORDENAMIENTO
        # =================================================

        self.combo_orden = QComboBox()

        self.combo_orden.addItem("Ordenar por Prioridad", "prioridad")
        self.combo_orden.addItem("Ordenar por Peso",      "peso")

        busqueda_layout.addRow("Orden:", self.combo_orden)

        # =================================================
        # BOTONES BUSQUEDA
        # =================================================

        btn_buscar  = QPushButton("Buscar")
        btn_ordenar = QPushButton("Ordenar Lista")

        btn_buscar.clicked.connect(self.buscar_pedido)
        btn_ordenar.clicked.connect(self.ordenar_pedidos)

        busqueda_layout.addRow(btn_buscar)
        busqueda_layout.addRow(btn_ordenar)

        layout.addWidget(busqueda_group)

        # =================================================
        # =================================================
        # SECCION ALGORITMOS
        # =================================================
        # =================================================

        algoritmos_group = QGroupBox("ALGORITMOS")

        algoritmos_layout = QVBoxLayout()

        algoritmos_group.setLayout(algoritmos_layout)

        btn_greedy      = QPushButton("Asignar Pedidos (Greedy)")
        btn_backtracking = QPushButton("Optimizar Ruta (Backtracking)")
        btn_divide      = QPushButton("Segmentar Ciudad (Divide y Vencerás)")
        btn_dinamica    = QPushButton("Cargar Vehiculo (Prog. Dinámica)")

        btn_greedy.clicked.connect(self.ejecutar_greedy)
        btn_backtracking.clicked.connect(self.ejecutar_backtracking)
        btn_divide.clicked.connect(self.ejecutar_divide)
        btn_dinamica.clicked.connect(self.ejecutar_dinamica)

        algoritmos_layout.addWidget(btn_greedy)
        algoritmos_layout.addWidget(btn_backtracking)
        algoritmos_layout.addWidget(btn_divide)
        algoritmos_layout.addWidget(btn_dinamica)

        layout.addWidget(algoritmos_group)

        # =================================================
        # =================================================
        # SECCION COMPLEJIDADES
        # =================================================
        # =================================================

        complejidades_group = QGroupBox("COMPLEJIDADES")

        complejidades_layout = QVBoxLayout()

        complejidades_group.setLayout(complejidades_layout)

        btn_comp_greedy      = QPushButton("Complejidad Greedy")
        btn_comp_backtracking = QPushButton("Complejidad Backtracking")
        btn_comp_divide      = QPushButton("Complejidad Divide y Vencerás")
        btn_comp_dinamica    = QPushButton("Complejidad Prog. Dinámica")

        btn_comp_greedy.clicked.connect(self.mostrar_complejidad_greedy)
        btn_comp_backtracking.clicked.connect(self.mostrar_complejidad_backtracking)
        btn_comp_divide.clicked.connect(self.mostrar_complejidad_divide)
        btn_comp_dinamica.clicked.connect(self.mostrar_complejidad_dinamica)

        complejidades_layout.addWidget(btn_comp_greedy)
        complejidades_layout.addWidget(btn_comp_backtracking)
        complejidades_layout.addWidget(btn_comp_divide)
        complejidades_layout.addWidget(btn_comp_dinamica)

        layout.addWidget(complejidades_group)

        layout.addStretch()


    # =====================================================
    # CARGAR GRAFO
    # =====================================================

    def cargar_grafo(self):

        progreso = QProgressDialog(
            "Descargando grafo de calles de Cusco...",
            None,
            0, 0,
            self
        )

        progreso.setWindowTitle("Cargando Grafo")

        progreso.setWindowModality(Qt.WindowModal)

        progreso.show()

        from PyQt5.QtWidgets import QApplication

        QApplication.processEvents()

        gestor = GestorGrafo.obtener_instancia()

        gestor.descargar()

        progreso.close()

        QMessageBox.information(
            self,
            "Grafo Cargado",
            f"Grafo de Cusco cargado correctamente.\n\n"
            f"Nodos (intersecciones): {gestor.grafo.number_of_nodes()}\n"
            f"Aristas (calles): {gestor.grafo.number_of_edges()}"
        )


    # =====================================================
    # MOSTRAR CALLES DEL GRAFO EN EL MAPA
    # =====================================================

    def mostrar_grafo(self):

        gestor = GestorGrafo.obtener_instancia()

        if not gestor.cargado:

            QMessageBox.warning(
                self,
                "Error",
                "Primero debes cargar el grafo de Cusco"
            )

            return

        if self.mapa is not None:

            self.mapa.dibujar_grafo()

            QMessageBox.information(
                self,
                "Grafo",
                "Calles reales de Cusco dibujadas en el mapa"
            )


    # =====================================================
    # REGISTRAR PEDIDO
    # =====================================================

    def registrar_pedido(self):

        cliente   = self.input_cliente.text()

        direccion = self.input_direccion.text()

        latitud   = self.input_latitud.value()

        longitud  = self.input_longitud.value()

        prioridad = self.input_prioridad.currentData()

        peso      = self.input_peso.value()

        if not cliente:

            QMessageBox.warning(self, "Error", "Ingrese el nombre del cliente")

            return

        if not direccion:

            QMessageBox.warning(self, "Error", "Ingrese la dirección")

            return

        nuevo_pedido = Pedido(
            self.id_actual_pedido,
            cliente,
            direccion,
            latitud,
            longitud,
            prioridad,
            peso
        )

        # =================================================
        # ASIGNAR NODO DEL GRAFO SI ESTA CARGADO
        # =================================================

        gestor = GestorGrafo.obtener_instancia()

        if gestor.cargado:

            nuevo_pedido.nodo_grafo = gestor.nodo_cercano(latitud, longitud)

        agregar_pedido(nuevo_pedido)

        print("PEDIDO REGISTRADO:")
        print(nuevo_pedido.mostrar_info())

        self.id_actual_pedido += 1

        # =================================================
        # LIMPIAR FORMULARIO
        # =================================================

        self.input_cliente.clear()
        self.input_direccion.clear()
        self.input_latitud.setValue(0)
        self.input_longitud.setValue(0)
        self.input_peso.setValue(0)
        self.input_prioridad.setCurrentIndex(0)

        QMessageBox.information(
            self,
            "Pedido Registrado",
            "El pedido fue registrado correctamente"
        )


    # =====================================================
    # BUSCAR PEDIDO
    # =====================================================

    def buscar_pedido(self):

        texto = self.input_busqueda.text().strip()

        tipo  = self.combo_busqueda.currentData()

        if not texto:

            QMessageBox.warning(self, "Error", "Ingrese un término de búsqueda")

            return

        if tipo == "id":

            try:

                pedido = buscar_pedido(int(texto))

                if pedido:

                    QMessageBox.information(
                        self,
                        "Pedido Encontrado",
                        pedido.mostrar_info()
                    )

                else:

                    QMessageBox.warning(
                        self,
                        "No encontrado",
                        f"No existe un pedido con ID {texto}"
                    )

            except ValueError:

                QMessageBox.warning(self, "Error", "El ID debe ser un número")

        elif tipo == "sector":

            resultado = buscar_pedidos_por_sector(texto)

            if resultado:

                info = "\n".join([
                    f"ID {p.id_pedido} - {p.cliente} ({p.direccion})"
                    for p in resultado
                ])

                QMessageBox.information(
                    self,
                    f"Pedidos en '{texto}'",
                    f"{len(resultado)} pedido(s) encontrado(s):\n\n{info}"
                )

            else:

                QMessageBox.warning(
                    self,
                    "No encontrado",
                    f"No hay pedidos en el sector '{texto}'"
                )


    # =====================================================
    # ORDENAR PEDIDOS
    # =====================================================

    def ordenar_pedidos(self):

        criterio = self.combo_orden.currentData()

        if criterio == "prioridad":

            pedidos.sort(
                key=lambda p: p.prioridad,
                reverse=True
            )

            QMessageBox.information(
                self,
                "Ordenamiento",
                "Pedidos ordenados por prioridad (mayor a menor)\n\n"
                + "\n".join([
                    f"ID {p.id_pedido} | Prioridad {p.prioridad} | {p.cliente}"
                    for p in pedidos
                ])
            )

        elif criterio == "peso":

            pedidos.sort(
                key=lambda p: p.peso,
                reverse=True
            )

            QMessageBox.information(
                self,
                "Ordenamiento",
                "Pedidos ordenados por peso (mayor a menor)\n\n"
                + "\n".join([
                    f"ID {p.id_pedido} | {p.peso} kg | {p.cliente}"
                    for p in pedidos
                ])
            )


    # =====================================================
    # VALIDAR GRAFO CARGADO
    # =====================================================

    def _validar_grafo(self):

        gestor = GestorGrafo.obtener_instancia()

        if not gestor.cargado:

            QMessageBox.warning(
                self,
                "Error",
                "Primero debes cargar el grafo de Cusco\n"
                "(boton 'Cargar Grafo de Cusco')"
            )

            return False

        return True


    # =====================================================
    # EJECUTAR GREEDY
    # =====================================================

    def ejecutar_greedy(self):

        if not self._validar_grafo():

            return

        if len(pedidos) == 0:

            QMessageBox.warning(self, "Error", "No existen pedidos registrados")

            return

        # =================================================
        # PEDIDO CON MAYOR PRIORIDAD
        # =================================================

        pedido_prioritario = max(pedidos, key=lambda p: p.prioridad)

        print(f"""
            ======================================
            PEDIDO PRIORITARIO
            ======================================
            ID:        {pedido_prioritario.id_pedido}
            Cliente:   {pedido_prioritario.cliente}
            Prioridad: {pedido_prioritario.prioridad}
        """)

        # =================================================
        # EJECUTAR GREEDY
        # =================================================

        repartidor, distancia = seleccionar_repartidor_greedy(

            pedido_prioritario.nodo_grafo
        )

        print(f"""
            ======================================
            REPARTIDOR ASIGNADO
            ======================================
            Nombre:    {repartidor.nombre}
            Distancia: {round(distancia, 1)} m
        """)

        # =================================================
        # DIBUJAR RUTA
        # =================================================

        if self.mapa is not None:

            self.mapa.mostrar_ruta_greedy(repartidor, pedido_prioritario)

        QMessageBox.information(
            self,
            "Greedy - Pedido Asignado",
            f"Pedido:      {pedido_prioritario.cliente}\n"
            f"Repartidor:  {repartidor.nombre}\n"
            f"Vehiculo:    {repartidor.vehiculo}\n"
            f"Distancia:   {round(distancia, 1)} m (por calles)"
        )


    # =====================================================
    # EJECUTAR BACKTRACKING
    # =====================================================

    def ejecutar_backtracking(self):

        if not self._validar_grafo():

            return

        if len(pedidos) < 2:

            QMessageBox.warning(self, "Error", "Se necesitan al menos 2 pedidos")

            return

        # =================================================
        # LIMITE DE SEGURIDAD  O(n!)
        # =================================================

        MAX_INTERMEDIOS = 8

        id_origen  = pedidos[0].id_pedido

        id_destino = pedidos[-1].id_pedido

        ids_permitidos = [p.id_pedido for p in pedidos[:MAX_INTERMEDIOS + 2]]

        if len(pedidos) > MAX_INTERMEDIOS + 2:

            QMessageBox.information(
                self,
                "Backtracking",
                f"Hay {len(pedidos)} pedidos.\n"
                f"Por ser O(n!), se usarán los primeros {MAX_INTERMEDIOS + 2}."
            )

        # =================================================
        # SECTORES BLOQUEADOS
        # =================================================

        sectores_bloqueados = ["Santiago", "Picchu"]

        # =================================================
        # EJECUTAR
        # =================================================

        rutas, mejor_ruta = buscar_rutas_backtracking(
            id_origen,
            id_destino,
            sectores_bloqueados,
            ids_permitidos
        )

        if mejor_ruta is None:

            QMessageBox.warning(self, "Backtracking", "No se encontraron rutas válidas")

            return

        print(f"""
            ======================================
            BACKTRACKING
            ======================================
            Rutas evaluadas:  {len(rutas)}
            Distancia minima: {round(mejor_ruta['distancia'], 1)} m
        """)

        if self.mapa is not None:

            self.mapa.mostrar_ruta_backtracking(mejor_ruta["ruta"])

        QMessageBox.information(
            self,
            "Backtracking - Ruta Óptima",
            f"Rutas evaluadas:  {len(rutas)}\n"
            f"Distancia mínima: {round(mejor_ruta['distancia'], 1)} m\n"
            f"Sectores evitados: {', '.join(sectores_bloqueados)}"
        )


    # =====================================================
    # EJECUTAR DIVIDE Y VENCERAS
    # =====================================================

    def ejecutar_divide(self):

        if not self._validar_grafo():

            return

        if len(pedidos) == 0:

            QMessageBox.warning(self, "Error", "No existen pedidos registrados")

            return

        centro_lat, centro_lon, cuadrantes = segmentar_ciudad()

        print(f"""
            ======================================
            DIVIDE Y VENCERAS
            ======================================
            Centro: ({round(centro_lat,4)}, {round(centro_lon,4)})
            NO: {len(cuadrantes['NO'])} pedidos
            NE: {len(cuadrantes['NE'])} pedidos
            SO: {len(cuadrantes['SO'])} pedidos
            SE: {len(cuadrantes['SE'])} pedidos
        """)

        if self.mapa is not None:

            self.mapa.mostrar_cuadrantes(centro_lat, centro_lon, cuadrantes)

        QMessageBox.information(
            self,
            "Divide y Vencerás - Cuadrantes",
            f"Ciudad segmentada en 4 cuadrantes\n\n"
            f"NO (Nor-Oeste): {len(cuadrantes['NO'])} pedidos\n"
            f"NE (Nor-Este):  {len(cuadrantes['NE'])} pedidos\n"
            f"SO (Sur-Oeste): {len(cuadrantes['SO'])} pedidos\n"
            f"SE (Sur-Este):  {len(cuadrantes['SE'])} pedidos"
        )


    # =====================================================
    # EJECUTAR PROGRAMACION DINAMICA (MOCHILA)
    # =====================================================

    def ejecutar_dinamica(self):

        if len(pedidos) == 0:

            QMessageBox.warning(self, "Error", "No existen pedidos registrados")

            return

        # =================================================
        # ELEGIR REPARTIDOR DE MAYOR CAPACIDAD
        # =================================================

        repartidor = max(repartidores, key=lambda r: r.capacidad_maxima)

        seleccionados, valor_total, peso_total = resolver_mochila(

            repartidor.capacidad_maxima
        )

        print(f"""
            ======================================
            PROGRAMACION DINAMICA (MOCHILA)
            ======================================
            Repartidor:   {repartidor.nombre}
            Capacidad:    {repartidor.capacidad_maxima} kg
            Pedidos:      {len(seleccionados)}
            Valor total:  {valor_total}
            Peso usado:   {peso_total} kg
        """)

        if self.mapa is not None:

            self.mapa.mostrar_mochila(seleccionados)

        QMessageBox.information(
            self,
            "Prog. Dinámica - Carga Óptima",
            f"Repartidor:      {repartidor.nombre}\n"
            f"Capacidad:       {repartidor.capacidad_maxima} kg\n\n"
            f"Pedidos cargados: {len(seleccionados)}\n"
            f"Prioridad total:  {valor_total}\n"
            f"Peso usado:       {peso_total} kg"
        )


    # =====================================================
    # MOSTRAR COMPLEJIDAD GREEDY
    # =====================================================

    def mostrar_complejidad_greedy(self):

        ventana = VentanaComplejidadGreedy(parent=self)

        ventana.exec_()


    # =====================================================
    # MOSTRAR COMPLEJIDAD BACKTRACKING
    # =====================================================

    def mostrar_complejidad_backtracking(self):

        ventana = VentanaComplejidadBacktracking(parent=self)

        ventana.exec_()


    # =====================================================
    # MOSTRAR COMPLEJIDAD DIVIDE Y VENCERAS
    # =====================================================

    def mostrar_complejidad_divide(self):

        ventana = VentanaComplejidadDivide(parent=self)

        ventana.exec_()


    # =====================================================
    # MOSTRAR COMPLEJIDAD PROG. DINAMICA
    # =====================================================

    def mostrar_complejidad_dinamica(self):

        ventana = VentanaComplejidadDinamica(parent=self)

        ventana.exec_()
