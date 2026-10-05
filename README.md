# restaurante_app — Semana 16

**Estudiante:** José Alberto Tarco Tipán  
**Materia:** Programación Orientada a Objetos  
**Institución:** Universidad Estatal Amazónica  
**Entrega:** Semana 16 — Interacción con eventos en Tkinter

---

## 1. Descripción general

Esta entrega evoluciona `restaurante_app` (Parrilla del Valle) a partir de la Semana 15, sin reconstruirla. Se conservan íntegramente el inicio de sesión, la navegación, la gestión completa del menú y la sección Ventas ya construidas con `command=`.

El objetivo central de esta semana es avanzar del uso básico de `command=` hacia el **manejo real de eventos de Tkinter mediante `bind()`**: responder a la selección en una tabla, a teclas del teclado y al cambio de valor en un `Combobox`, sin concentrar lógica de negocio en la interfaz.

Como caso práctico, la sección **Usuarios** —que hasta la Semana 15 solo permitía consultar clientes— se convierte en una gestión completa (CRUD) con **roles** (`Administrador`, `Empleado`, `Cliente`) y control de acceso básico: solo el rol `Administrador` puede ver y usar esta sección.

---

## 2. Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

La estructura no cambió respecto a la Semana 15. La evolución ocurre en `modelos/usuario.py` (atributo `rol`), `restaurante_servicio.py` (CRUD de usuarios) y `ui/main_view.py` (sección Usuarios con formulario, tabla y eventos).

---

## 3. Responsabilidad de cada capa

| Capa | Responsabilidad |
|---|---|
| `modelos/` | `Producto` (con tiempo de preparación), `Venta` (relaciona `usuario_identificacion`, `producto_codigo` y `fecha`) y `Usuario`, ahora con el atributo `rol`, validado mediante `property` contra `ROLES_PERMITIDOS = (Administrador, Empleado, Cliente)`. |
| `servicios/archivo_servicio.py` | Lee y escribe los archivos JSON de `datos/`. |
| `servicios/restaurante_servicio.py` | Convierte los datos en objetos, valida el acceso y expone el CRUD completo de platos y ventas, además del **CRUD completo de usuarios** (nuevo): `registrar_usuario`, `actualizar_usuario`, `eliminar_usuario`, `buscar_usuario_por_login`. Toda la validación y persistencia vive aquí, nunca en la interfaz. |
| `ui/` | `LoginView` y `MainView`, construidas con Tkinter; solicitan las operaciones a `RestauranteServicio` y responden a eventos de Tkinter sin tocar el JSON directamente. |
| `main.py` | Crea la única ventana principal, configura el ícono del sistema desde `assets/` y controla el cambio entre vistas. No se modificó esta semana. |

---

## 4. Componentes y contenedores utilizados

- `Frame`: separa encabezado, barra de navegación, contenido y barra de estado.
- `LabelFrame`: agrupa el formulario ("Datos del plato" / "Datos del usuario"), el listado ("Platos del menu" / "Usuarios registrados") y "Registrar pedido" / "Ventas registradas".
- `Entry`: código, nombre y precio del plato; identificación, nombre, mesa y usuario del cliente o empleado; credenciales de acceso.
- `ttk.Combobox` (solo lectura): selector de categoría del plato, selector de cliente y de plato en Ventas, y ahora selector de **rol** en Usuarios.
- `ttk.Spinbox`: selectores numéricos para el tiempo de preparación (minutos) y el stock del plato.
- `ttk.Treeview` + `ttk.Scrollbar`: tablas de platos, ventas y usuarios (ahora con columna Rol), con desplazamiento vertical.
- `ttk.Button` / `ttk.Style`: botones de acción conectados mediante `command=`, con íconos de `assets/icons/`.
- Gestores de geometría: `pack()` para la estructura general y `grid()` dentro de los formularios.

---

## 5. Manejo de eventos con `bind()` (nuevo — Semana 16)

La sección **Usuarios** es el ejemplo principal de esta entrega para el manejo de eventos reales de Tkinter, más allá de `command=`:

```
Interaccion del usuario -> evento -> bind() -> callback(event) -> RestauranteServicio -> usuarios.json -> tabla actualizada
```

| Evento | Widget | Callback | Efecto |
|---|---|---|---|
| `<<TreeviewSelect>>` | Tabla de usuarios | `al_seleccionar_usuario` | Carga el usuario seleccionado en el formulario |
| `<Return>` | Contraseña / Rol | `al_presionar_enter_usuario` | Registra el usuario desde el formulario |
| `<Escape>` | Todos los campos y la tabla | `al_presionar_escape_usuario` | Limpia el formulario y cancela la selección |
| `<<ComboboxSelected>>` | Combobox de rol | `al_seleccionar_rol` | Actualiza la etiqueta "Rol seleccionado" |

Ningún callback contiene lógica de negocio: todos obtienen datos de la interfaz o del `event` recibido y delegan la validación y la persistencia a `RestauranteServicio`, reutilizando exactamente el mismo patrón que ya usaba la sección Ventas con `command=`.

---

## 6. Sección Ventas: flujo de eventos con `command=` (Semana 15)

```
Cliente elige un Cliente y un Plato en los Combobox
                ↓
Clic en "Registrar venta"  (command=self.registrar_venta)
                ↓
Callback registrar_venta() en MainView:
    - obtiene el texto seleccionado en cada Combobox
    - lo traduce a la identificacion / codigo real
    - llama a restaurante_servicio.registrar_venta(...)
                ↓
RestauranteServicio.registrar_venta():
    - valida que ambos campos vengan seleccionados
    - valida que el cliente exista
    - valida que el plato exista
    - crea un objeto Venta (el modelo valida sus propios datos)
    - agrega la venta en memoria y llama a guardar_ventas()
                ↓
ArchivoServicio.escribir_json() persiste en ventas.json
                ↓
MainView.refrescar_ventas() actualiza la tabla (Treeview)
y la barra de estado inferior
```

Esta sección se conserva sin cambios; convive con la sección Usuarios como ejemplo de la diferencia entre `command=` (acción explícita de un botón) y `bind()` (respuesta a un evento generado por el usuario).

---

## 7. Gestión de usuarios y roles (nuevo — Semana 16)

La pestaña **Usuarios** del menú superior solo aparece cuando la sesión activa pertenece al rol `Administrador`; ese es el control de acceso básico que pide la actividad. Desde allí se puede:

- Registrar un nuevo usuario indicando identificación, nombre, mesa, usuario, contraseña y rol.
- Consultar los usuarios registrados en una tabla (`Treeview`), incluyendo su rol.
- Seleccionar un usuario de la tabla (evento `<<TreeviewSelect>>`) para cargar automáticamente sus datos en el formulario.
- Actualizar los datos del usuario seleccionado.
- Eliminar el usuario seleccionado, con confirmación previa.
- Limpiar el formulario y cancelar la selección actual (botón o tecla `Escape`).

`RestauranteServicio` impide eliminar el usuario con el que se inició sesión y cambiar el rol del administrador actualmente conectado, para que la aplicación nunca quede sin una cuenta administrativa activa.

| Operación | Acción en la interfaz | Método en `RestauranteServicio` |
|---|---|---|
| Registrar usuario | Botón **Registrar** / tecla `Enter` | `registrar_usuario(identificacion, nombre, mesa, usuario, contrasena, rol)` |
| Consultar usuario | Selección en la tabla (`<<TreeviewSelect>>`) | `buscar_usuario_por_identificacion(identificacion)` |
| Actualizar usuario | Botón **Actualizar** | `actualizar_usuario(identificacion, nombre, mesa, usuario, contrasena, rol, identificacion_actual)` |
| Eliminar usuario | Botón **Eliminar** | `eliminar_usuario(identificacion, identificacion_actual)` |

---

## 8. Operaciones implementadas sobre el menú y las ventas

| Operación | Acción en la interfaz | Método en `RestauranteServicio` |
|---|---|---|
| Registrar plato | Botón **Registrar** | `registrar_producto(codigo, nombre, precio, categoria, tiempo_preparacion, stock)` |
| Consultar plato | Botón **Cargar / Consultar** | `buscar_producto_por_codigo(codigo)` |
| Actualizar plato | Botón **Actualizar** | `actualizar_producto(codigo, nombre, precio, categoria, tiempo_preparacion, stock)` |
| Eliminar plato | Botón **Eliminar** | `eliminar_producto(codigo)` |
| Registrar venta | Botón **Registrar venta** | `registrar_venta(usuario_identificacion, producto_codigo)` |

Todas las validaciones (campos vacíos, precio o tiempo no numérico, categoría inválida, código duplicado, cliente o plato inexistente, rol inválido, usuario o identificación duplicados) se resuelven en los modelos y en `RestauranteServicio`; la interfaz solo captura los datos y muestra el resultado con `messagebox`.

---

## 9. Recursos gráficos (`assets/`)

- `assets/logo/logo.png`: logotipo mostrado en la pantalla de inicio de sesión.
- `assets/logo/icono.png`: versión simplificada usada como ícono de la ventana principal y junto al título en el encabezado.
- `assets/icons/`: íconos para cada botón de navegación (Inicio, Productos, Usuarios, Ventas, Pedidos, Cerrar sesión) y para las acciones de los formularios (Registrar, Consultar/Cargar, Actualizar, Eliminar, Limpiar), reutilizados también en el nuevo formulario de usuarios (`add.png`, `edit.png`, `delete.png`, `clean.png`).

---

## 10. Persistencia

Los cambios sobre el menú se guardan en `datos/productos.json` mediante `guardar_productos()`. Las ventas se guardan en `datos/ventas.json` mediante `guardar_ventas()`. Los usuarios se guardan en `datos/usuarios.json` mediante `guardar_usuarios()` (nuevo), incluyendo ahora el campo `rol`. Las tres operaciones delegan en `ArchivoServicio`. Al reabrir la aplicación, los platos, las ventas y los usuarios registrados se conservan.

Ejemplo de usuario persistido:

```json
{
    "identificacion": "1807654321",
    "nombre": "Mesero Principal",
    "mesa": "Salon",
    "usuario": "mesero1",
    "contrasena": "mesa2026",
    "rol": "Empleado"
}
```

---

## 11. Control de acceso

| Rol | Acceso a la pestaña Usuarios |
|---|---|
| `Administrador` | Sí |
| `Empleado` | No |
| `Cliente` | No |

No se implementa un sistema avanzado de permisos; el objetivo es demostrar un control de acceso básico a partir del rol del usuario que inició sesión.

---

## 12. Flujo de la aplicación

```
Inicio de la aplicacion
        ↓
main.py prepara Tkinter, el icono del sistema y los servicios
        ↓
LoginView (usuario y clave)
        ↓
RestauranteServicio valida el acceso
        ↓
MainView
        ↓
Inicio (resumen) | Productos (menu) | Usuarios* (solo Administrador) | Ventas (pedidos) | Pedidos
        ↓
Usuarios: seleccionar una fila -> <<TreeviewSelect>> -> formulario cargado
        ↓
Registrar / Actualizar / Eliminar -> command= -> RestauranteServicio valida y persiste
        ↓
Enter registra, Escape limpia, <<ComboboxSelected>> actualiza el rol mostrado
        ↓
Actualizacion de la tabla de usuarios y de la barra de estado
```

---

## 13. Credenciales de acceso (demostración)

| Usuario | Contraseña | Rol |
|---|---|---|
| `jtarco` | `grill2026` | Cliente |
| `admin` | `admin456` | Administrador |
| `mesero1` | `mesa2026` | Empleado |

La contraseña debe incluir al menos un número, según la validación del modelo `Usuario`.

---

## 14. Ejecución

```bash
cd restaurante_app
python main.py
```

Requiere **Python 3.10 o superior** y Tkinter disponible en la instalación.

---

## 15. Pruebas realizadas

1. Se ejecutó `main.py` y la aplicación inició sin errores, con el ícono del sistema visible en la ventana.
2. El acceso con `admin` / `admin456` continúa funcionando y muestra el logotipo.
3. La interfaz principal y la gestión completa de Productos siguen funcionando igual que en la Semana 15.
4. Con la sesión de `admin`, aparece la pestaña **Usuarios**; con `jtarco` (Cliente), la pestaña no aparece en el menú superior.
5. Se registró un nuevo usuario con rol `Empleado` desde el formulario; apareció de inmediato en la tabla.
6. Al seleccionar una fila de la tabla (`<<TreeviewSelect>>`), los datos se cargaron correctamente en el formulario.
7. Se actualizaron el nombre, la contraseña y el rol de un usuario seleccionado; el cambio se reflejó en la tabla y en `usuarios.json`.
8. Se intentó cambiar el rol del administrador con el que se inició sesión: la operación fue rechazada con un mensaje claro.
9. Se intentó eliminar el usuario con el que se inició sesión: la operación fue rechazada.
10. Se usó la tecla `Enter` desde el campo Contraseña para registrar un usuario, y `Escape` para limpiar el formulario y cancelar la selección.
11. El Combobox de rol actualizó la etiqueta "Rol seleccionado" al cambiar de valor (`<<ComboboxSelected>>`).
12. La sección Ventas se probó sin cambios y continúa registrando pedidos mediante `command=`.
13. Al cerrar y volver a ejecutar la aplicación, los usuarios, productos y ventas registrados se recuperan correctamente.

---

## 16. Nota educativa sobre autenticación

El acceso de esta etapa es una simulación pedagógica. Las contraseñas se guardan en JSON en texto plano solo con fines didácticos; no representa una práctica segura para un sistema real. La gestión de roles tampoco implementa un sistema de permisos avanzado: su propósito es mostrar, de forma clara, el uso de eventos de Tkinter aplicados a una operación CRUD real.
