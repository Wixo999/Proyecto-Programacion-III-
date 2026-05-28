# =========================================================
# CLASE PEDIDO
# =========================================================

class Pedido:

    def __init__(
        self,
        id_pedido,
        cliente,
        direccion,
        latitud,
        longitud,
        prioridad,
        peso
    ):

        # =================================================
        # DATOS BASICOS
        # =================================================

        self.id_pedido  = id_pedido

        self.cliente    = cliente

        self.direccion  = direccion

        # =================================================
        # COORDENADAS
        # =================================================

        self.latitud  = latitud

        self.longitud = longitud

        # =================================================
        # PRIORIDAD
        #
        # 1 = baja
        # 2 = media
        # 3 = urgente
        # =================================================

        self.prioridad = prioridad

        # =================================================
        # PESO
        #
        # Para Programacion Dinamica
        # Problema Mochila
        # =================================================

        self.peso = peso

        # =================================================
        # ESTADO
        # =================================================

        self.entregado = False

        # =================================================
        # NODO DEL GRAFO MAS CERCANO
        #
        # Se asigna al inicializar el grafo.
        # Permite trabajar con calles reales de Cusco.
        # =================================================

        self.nodo_grafo = None

    # =====================================================
    # MOSTRAR INFORMACION
    # =====================================================

    def mostrar_info(self):

        return f"""

        ID:          {self.id_pedido}

        Cliente:     {self.cliente}

        Direccion:   {self.direccion}

        Coordenadas: ({self.latitud}, {self.longitud})

        Prioridad:   {self.prioridad}

        Peso:        {self.peso} kg

        Entregado:   {self.entregado}

        """


# =========================================================
# PEDIDOS DE PRUEBA
#
# DISTRIBUIDOS POR DISTINTAS ZONAS DE CUSCO
# =========================================================

pedidos = [

    Pedido(1,  "Carlos Quispe",   "San Blas",       -13.5135, -71.9722, 4,  5),
    Pedido(2,  "Maria Flores",    "Wanchaq",         -13.5250, -71.9670, 2,  8),
    Pedido(3,  "Jose Huaman",     "Santiago",        -13.5310, -71.9810, 1, 12),
    Pedido(4,  "Lucia Ramos",     "Ttio",            -13.5220, -71.9560, 3,  7),
    Pedido(5,  "Andres Perez",    "Magisterio",      -13.5190, -71.9500, 2,  4),
    
]


# =========================================================
# FUNCION AGREGAR PEDIDO
# =========================================================

def agregar_pedido(pedido):

    pedidos.append(pedido)


# =========================================================
# FUNCION BUSCAR PEDIDO POR ID
# =========================================================

def buscar_pedido(id_pedido):

    for pedido in pedidos:

        if pedido.id_pedido == id_pedido:

            return pedido

    return None


# =========================================================
# FUNCION BUSCAR PEDIDOS POR SECTOR
# =========================================================

def buscar_pedidos_por_sector(sector):

    resultado = []

    for pedido in pedidos:

        if sector.lower() in pedido.direccion.lower():

            resultado.append(pedido)

    return resultado


# =========================================================
# FUNCION MOSTRAR PEDIDOS
# =========================================================

def mostrar_pedidos():

    for pedido in pedidos:

        print(pedido.mostrar_info())
