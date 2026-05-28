# =========================================================
# CLASE REPARTIDOR
# =========================================================

class Repartidor:

    def __init__(
        self,
        id_repartidor,
        nombre,
        vehiculo,
        capacidad_maxima,
        latitud,
        longitud
    ):

        # =================================================
        # DATOS BASICOS
        # =================================================

        self.id_repartidor = id_repartidor

        self.nombre        = nombre

        # =================================================
        # VEHICULO
        #
        # moto
        # bicicleta
        # camioneta
        # =================================================

        self.vehiculo = vehiculo

        # =================================================
        # CAPACIDAD MAXIMA
        # =================================================

        self.capacidad_maxima = capacidad_maxima

        # =================================================
        # PEDIDOS ASIGNADOS
        # =================================================

        self.pedidos_asignados = []

        # =================================================
        # POSICION ACTUAL
        # =================================================

        self.latitud_actual  = latitud

        self.longitud_actual = longitud

        # =================================================
        # NODO DEL GRAFO MAS CERCANO
        #
        # Se asigna al inicializar el grafo.
        # =================================================

        self.nodo_grafo = None

    # =====================================================
    # ASIGNAR PEDIDO
    # =====================================================

    def asignar_pedido(self, pedido):

        self.pedidos_asignados.append(pedido)

    # =====================================================
    # CALCULAR CARGA ACTUAL
    # =====================================================

    def carga_actual(self):

        total = 0

        for pedido in self.pedidos_asignados:

            total += pedido.peso

        return total

    # =====================================================
    # VERIFICAR CAPACIDAD
    # =====================================================

    def puede_cargar(self, pedido):

        return (
            self.carga_actual() + pedido.peso
            <=
            self.capacidad_maxima
        )

    # =====================================================
    # MOSTRAR INFO
    # =====================================================

    def mostrar_info(self):

        return f"""

        ID:              {self.id_repartidor}

        Nombre:          {self.nombre}

        Vehiculo:        {self.vehiculo}

        Capacidad Max:   {self.capacidad_maxima} kg

        Coordenadas:     ({self.latitud_actual}, {self.longitud_actual})

        """


# =========================================================
# LISTA GLOBAL DE REPARTIDORES
# =========================================================

repartidores = [

    Repartidor(1,  "Luis Herrera",      "Moto",      20, -13.5160, -71.9780),
    Repartidor(2,  "Ana Quispe",        "Bicicleta", 10, -13.5250, -71.9670),
    Repartidor(3,  "Carlos Ramos",      "Moto",      18, -13.5310, -71.9500),
    Repartidor(4,  "Maria Flores",      "Moto",      15, -13.5100, -71.9900),
    Repartidor(5,  "Pedro Huaman",      "Camioneta", 40, -13.5050, -71.9700),
    Repartidor(6,  "Rosa Paredes",      "Moto",      20, -13.5400, -71.9800),
    Repartidor(7,  "Jorge Condori",     "Bicicleta", 12, -13.5155, -71.9600),
    Repartidor(8,  "Lucia Salas",       "Moto",      18, -13.5200, -71.9500),
    Repartidor(9,  "Miguel Torres",     "Moto",      22, -13.5000, -71.9750),
    Repartidor(10, "Diana Castro",      "Bicicleta",  8, -13.5480, -71.9690),
    Repartidor(11, "Fernando Luna",     "Moto",      20, -13.5350, -71.9400),
    Repartidor(12, "Carmen Ortiz",      "Moto",      16, -13.5180, -71.9850),
    Repartidor(13, "Alberto Vega",      "Camioneta", 35, -13.4950, -71.9650),
    Repartidor(14, "Sandra Molina",     "Moto",      19, -13.5280, -71.9900),
    Repartidor(15, "Ricardo Perez",     "Bicicleta", 10, -13.5450, -71.9500),
    Repartidor(16, "Patricia Rojas",    "Moto",      18, -13.5550, -71.9750),
    Repartidor(17, "Diego Cardenas",    "Moto",      20, -13.5120, -71.9450),
    Repartidor(18, "Elena Vargas",      "Camioneta", 45, -13.4900, -71.9800),
    Repartidor(19, "Raul Medina",       "Moto",      17, -13.5250, -71.9400),
    Repartidor(20, "Paola Chavez",      "Bicicleta",  9, -13.5380, -71.9600),
    Repartidor(21, "Andres Gutierrez",  "Moto",      20, -13.5480, -71.9900),
    Repartidor(22, "Natalia Cruz",      "Moto",      18, -13.5000, -71.9500),
    Repartidor(23, "Kevin Mendoza",     "Bicicleta", 11, -13.5600, -71.9700),
    Repartidor(24, "Silvia Navarro",    "Moto",      21, -13.5220, -71.9990),
    Repartidor(25, "Oscar Valdez",      "Camioneta", 50, -13.4850, -71.9550),
    Repartidor(26, "Monica Delgado",    "Moto",      16, -13.5350, -71.9550),
    Repartidor(27, "Javier Aguilar",    "Moto",      18, -13.5050, -71.9400),
    Repartidor(28, "Gabriela Pena",     "Bicicleta", 10, -13.5580, -71.9850),
    Repartidor(29, "Sergio Herrera",    "Moto",      20, -13.4950, -71.9900),
    Repartidor(30, "Valeria Campos",    "Moto",      19, -13.5420, -71.9450),
]


# =========================================================
# FUNCION MOSTRAR REPARTIDORES
# =========================================================

def mostrar_repartidores():

    for repartidor in repartidores:

        print(repartidor.mostrar_info())
