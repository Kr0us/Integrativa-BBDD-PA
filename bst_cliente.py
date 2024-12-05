# bst_cliente.py

class NodoCliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.contador = 1
        self.izquierdo = None
        self.derecho = None

class ArbolClientes:
    def __init__(self):
        self.raiz = None

    def insertar(self, id_cliente):
        self.raiz = self._insertar_recursivo(self.raiz, id_cliente)

    def _insertar_recursivo(self, nodo, id_cliente):
        if nodo is None:
            return NodoCliente(id_cliente)
        if id_cliente == nodo.id_cliente:
            nodo.contador += 1
        elif id_cliente < nodo.id_cliente:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, id_cliente)
        else:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, id_cliente)
        return nodo

    def encontrar_cliente_mas_frecuente(self):
        self.max_contador = 0
        self.cliente_mas_frecuente = None
        self._recorrer_inorden(self.raiz)
        return self.cliente_mas_frecuente, self.max_contador

    def _recorrer_inorden(self, nodo):
        if nodo:
            self._recorrer_inorden(nodo.izquierdo)
            if nodo.contador > self.max_contador:
                self.max_contador = nodo.contador
                self.cliente_mas_frecuente = nodo.id_cliente
            self._recorrer_inorden(nodo.derecho)