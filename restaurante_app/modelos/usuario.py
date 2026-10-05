class Usuario:
    LONGITUD_MINIMA_CONTRASENA: int = 4
    ROLES_PERMITIDOS: tuple[str, ...] = ("Administrador", "Empleado", "Cliente")

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        mesa: str,
        usuario: str,
        contrasena: str,
        rol: str = "Cliente",
    ) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.mesa = mesa
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion no puede estar vacia.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacio.")
        self._nombre = valor.strip()

    @property
    def mesa(self) -> str:
        return self._mesa

    @mesa.setter
    def mesa(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El numero de mesa no puede estar vacio.")
        self._mesa = valor.strip()

    @property
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre de usuario no puede estar vacio.")
        usuario_limpio = valor.strip()
        if " " in usuario_limpio:
            raise ValueError("El nombre de usuario no puede contener espacios.")
        self._usuario = usuario_limpio

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La contrasena no puede estar vacia.")
        valor_limpio = valor.strip()
        if len(valor_limpio) < self.LONGITUD_MINIMA_CONTRASENA:
            raise ValueError(
                f"La contrasena debe tener al menos {self.LONGITUD_MINIMA_CONTRASENA} caracteres."
            )
        if not any(caracter.isdigit() for caracter in valor_limpio):
            raise ValueError("La contrasena debe incluir al menos un numero.")
        self._contrasena = valor_limpio

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str) -> None:
        # Semana 16: restringe el rol a los valores definidos por el sistema.
        if not valor or not valor.strip():
            raise ValueError("El rol no puede estar vacio.")
        rol_limpio = valor.strip().capitalize()
        if rol_limpio not in self.ROLES_PERMITIDOS:
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )
        self._rol = rol_limpio

    def validar_credenciales(self, usuario: str, contrasena: str) -> bool:
        # Compara los datos de acceso ingresados con los del usuario actual.
        return self._usuario == usuario.strip() and self._contrasena == contrasena.strip()

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "mesa": self.mesa,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    def __str__(self) -> str:
        return (
            f"Identificacion: {self.identificacion} | "
            f"Nombre: {self.nombre} | Mesa: {self.mesa} | Rol: {self.rol}"
        )
