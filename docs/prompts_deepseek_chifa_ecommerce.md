# Prompts para DeepSeek — Plantilla E-commerce "Chifa" (Vue 3 + Django)

Guía de prompts secuenciales para que DeepSeek actúe como desarrollador full stack y construya la plantilla, inspirada en la estructura típica de sitios de delivery de restaurantes peruanos (tipo chifamyhome.pe): banner/hero, categorías de menú, catálogo de platos con modal de detalle, carrito lateral, checkout con delivery/recojo en tienda, métodos de pago locales (Yape/Plin/tarjeta/efectivo), selección de dirección/zona de reparto, y seguimiento de pedido.

Cada bloque de abajo es un prompt independiente y listo para copiar/pegar. Van en orden: primero defines el rol y el alcance (prompt maestro), luego backend, luego frontend, luego integración y despliegue. Pega los prompts uno por uno en una misma conversación con DeepSeek para que mantenga el contexto del proyecto.

---

## 0. Prompt maestro (rol + contexto del proyecto)

```
Actúa como un desarrollador full stack senior, experto en Python/Django (con Django REST Framework) y en JavaScript/Vue 3 (Composition API). Vas a construir conmigo, paso a paso y en varios mensajes, una PLANTILLA de e-commerce para un restaurante de comida chifa (fusión peruano-china), inspirada en la estructura funcional de sitios de delivery como chifamyhome.pe.

Reglas de trabajo:
- Responde siempre con código completo y funcional, no fragmentos incompletos ni "..." como relleno.
- Explica brevemente cada archivo antes de mostrarlo (2-4 líneas), no hace falta un ensayo.
- Usa buenas prácticas: separación de responsabilidades, nombres claros, comentarios solo donde aporten valor.
- Cuando falte una decisión de diseño, elige la opción más simple y estándar, y anótala en una línea al final como "Supuesto: ...".
- Vamos a avanzar en fases; en cada prompt te diré en qué fase estamos y qué debes construir exactamente. No adelantes fases futuras salvo que te lo pida.

STACK TÉCNICO:
- Backend: Python 3.11+, Django 5.x, Django REST Framework, PostgreSQL (SQLite solo para desarrollo local), django-cors-headers, djangorestframework-simplejwt para autenticación, Pillow para imágenes.
- Frontend: Vue 3 (Composition API + <script setup>), Vite, Vue Router, Pinia (estado global), Axios, TailwindCSS.
- Arquitectura: SPA en Vue consumiendo una API REST de Django. Backend también expone un panel de administración (Django Admin) para que el dueño del restaurante gestione categorías, platos, combos, promociones y pedidos.

ALCANCE FUNCIONAL DE LA PLANTILLA (inspirado en un e-commerce de chifa/delivery):
1. Home con banner/hero promocional, accesos a categorías destacadas y platos recomendados.
2. Catálogo de productos organizado por categorías (Entradas, Sopas, Arroces chaufa, Tallarines saltados, Wantanes, Combos/Promos, Bebidas, Postres).
3. Ficha/modal de producto con imagen, descripción, precio, variantes (tamaño: personal/mediano/familiar) y extras/adicionales.
4. Carrito de compras persistente (lateral tipo drawer), con edición de cantidades y subtotal en tiempo real.
5. Checkout con dos modalidades: Delivery (con dirección y referencia) y Recojo en tienda, cálculo de costo de envío por zona, selección de método de pago (Yape/Plin, tarjeta, efectivo contraentrega) y campo de comentarios/instrucciones.
6. Registro/login de cliente (opcional, se puede comprar como invitado) y sección "Mis pedidos" con historial y estado (Pendiente, Confirmado, En preparación, En camino, Entregado, Cancelado).
7. Panel de administración (Django Admin) para gestionar categorías, productos, combos, cupones de descuento, zonas de delivery, horarios de atención y pedidos entrantes.
8. Página de contacto/ubicación con horarios y enlace directo a WhatsApp para consultas.

Confírmame que entendiste el alcance y resume en una lista corta las apps de Django y los módulos de Vue que vas a crear, antes de escribir código. Espera mi mensaje "Fase 1" para empezar con el backend.
```

---

## FASE 1 — Backend: estructura del proyecto y modelos

### 1.1 Estructura inicial del proyecto Django

```
Fase 1.1 — Estructura del proyecto backend.

Crea la estructura inicial de un proyecto Django llamado "chifa_backend" con las siguientes apps:
- core (configuraciones generales, modelos abstractos base, horarios de atención, datos del restaurante)
- catalog (categorías, productos, variantes, extras, combos)
- orders (carrito, pedidos, items de pedido, cupones)
- delivery (zonas de reparto y costos de envío)
- accounts (usuarios personalizados basados en AbstractUser, direcciones guardadas)

Entrégame:
1. El árbol de carpetas completo del proyecto.
2. El archivo requirements.txt con las dependencias necesarias (Django, djangorestframework, django-cors-headers, djangorestframework-simplejwt, Pillow, psycopg2-binary, python-decouple).
3. El settings.py completo, incluyendo: INSTALLED_APPS con las apps anteriores, configuración de DRF (paginación, permisos por defecto), configuración de SimpleJWT, CORS_ALLOWED_ORIGINS para el frontend en desarrollo (http://localhost:5173), configuración de archivos MEDIA para imágenes de productos, y uso de python-decouple para variables de entorno (.env).
4. Un archivo .env.example con las variables necesarias.
```

### 1.2 Modelos — catálogo

```
Fase 1.2 — Modelos de la app "catalog".

Escribe el archivo catalog/models.py con los siguientes modelos:

- Category: nombre, slug, imagen, orden de visualización, activo (booleano).
- Product: nombre, slug, categoría (FK), descripción corta, descripción larga, imagen principal, precio base (Decimal), disponible (booleano), destacado (booleano, para mostrar en home), tiempo estimado de preparación en minutos, orden.
- ProductVariant: producto (FK), nombre (ej. "Personal", "Mediano", "Familiar"), precio (Decimal), es_default (booleano).
- ProductExtra: nombre del adicional (ej. "Wantán extra", "Salsa adicional"), precio, disponible (booleano), relación ManyToMany hacia Product (un extra puede aplicar a varios productos).
- Combo: nombre, slug, descripción, imagen, precio, activo, relación ManyToMany hacia Product para indicar qué platos incluye (con un campo intermedio "cantidad" usando un modelo through llamado ComboItem).

Requisitos:
- Usa un modelo abstracto TimeStampedModel en core/models.py (created_at, updated_at) y hereda de él en todos los modelos anteriores.
- Genera el slug automáticamente en el save() si no viene definido, usando django.utils.text.slugify.
- Agrega Meta con ordering apropiado en cada modelo.
- Incluye __str__ en todos los modelos.
- Después de los modelos, dame también core/models.py con el TimeStampedModel.
```

### 1.3 Modelos — pedidos, delivery y cuentas

```
Fase 1.3 — Modelos de "orders", "delivery" y "accounts".

1. accounts/models.py: modelo CustomUser (hereda de AbstractUser, agrega campo telefono) y modelo Address (usuario FK, alias como "Casa"/"Trabajo", dirección, referencia, distrito, es_default). Recuerda que CustomUser debe configurarse en settings.py con AUTH_USER_MODEL.

2. delivery/models.py: modelo DeliveryZone (nombre del distrito/zona, costo de envío, tiempo estimado de entrega en minutos, activo).

3. orders/models.py:
   - Coupon: código, tipo de descuento (porcentaje o monto fijo, usa choices), valor, fecha de inicio, fecha de expiración, uso máximo, veces usado, activo.
   - Order: usuario (FK nullable para permitir compra como invitado), nombre_contacto, telefono_contacto, tipo_entrega (choices: "delivery" / "recojo_tienda"), zona_delivery (FK nullable a DeliveryZone), direccion_entrega (texto, nullable), referencia, metodo_pago (choices: "yape_plin", "tarjeta", "efectivo"), estado (choices: pendiente, confirmado, en_preparacion, en_camino, entregado, cancelado; default pendiente), subtotal, costo_delivery, descuento, total, cupon (FK nullable a Coupon), comentarios, created_at.
   - OrderItem: pedido (FK related_name="items"), producto (FK), variante (FK nullable), cantidad, precio_unitario (snapshot del precio al momento de la compra), extras (ManyToMany hacia ProductExtra), subtotal_item.

Requisitos:
- Añade un método calcular_total() en el modelo Order que recalcule subtotal, descuento y total en base a sus items, costo de delivery y cupón aplicado.
- Añade validación con clean() para que si tipo_entrega es "delivery", direccion_entrega y zona_delivery sean obligatorios.
- Todos con TimeStampedModel donde aplique.
```

### 1.4 Django Admin

```
Fase 1.4 — Configuración del Django Admin.

Escribe los archivos admin.py de las apps catalog, orders, delivery y accounts, con las siguientes mejoras sobre el admin por defecto:

- catalog/admin.py: ProductAdmin con list_display (nombre, categoría, precio_base, disponible, destacado), list_filter por categoría y disponibilidad, search_fields por nombre, prepopulated_fields para el slug, e inlines para ProductVariant dentro de Product. CategoryAdmin con list_display y ordering editable inline (list_editable en "orden").
- orders/admin.py: OrderAdmin con list_display (id, nombre_contacto, tipo_entrega, estado, total, created_at), list_filter por estado y tipo_entrega, un inline OrderItemInline (readonly, TabularInline) para ver los items dentro del pedido, y una acción personalizada de admin "marcar_como_confirmado" que cambia el estado de los pedidos seleccionados.
- delivery/admin.py y accounts/admin.py: registro simple con list_display relevante; para CustomUser extiende UserAdmin de Django para incluir el campo telefono.

Dame el código completo de cada archivo admin.py.
```

---

## FASE 2 — Backend: API REST

### 2.1 Serializers

```
Fase 2.1 — Serializers de DRF.

Crea catalog/serializers.py con:
- CategorySerializer (todos los campos relevantes).
- ProductExtraSerializer.
- ProductVariantSerializer.
- ProductListSerializer (versión ligera para listados: id, nombre, slug, precio_base, imagen, categoría como string, destacado).
- ProductDetailSerializer (versión completa: incluye variantes anidadas y extras anidados, para la vista de detalle/modal de producto).
- ComboSerializer con sus items anidados (nombre del producto incluido y cantidad).

Crea orders/serializers.py con:
- OrderItemSerializer, incluyendo validación de que la cantidad sea mayor a 0.
- OrderCreateSerializer: usado para crear un pedido desde el checkout del frontend. Debe aceptar una lista de items (producto_id, variante_id opcional, cantidad, extras_ids opcionales), datos de contacto, tipo de entrega, dirección si aplica, método de pago, código de cupón opcional y comentarios. En el método create(), debe: calcular precios desde el backend (nunca confiar en precios enviados por el frontend), validar stock/disponibilidad, aplicar el cupón si es válido, calcular el costo de delivery según la zona, y crear el Order junto con sus OrderItems en una transacción atómica.
- OrderDetailSerializer: para mostrar el pedido completo con sus items (usado en confirmación y en "Mis pedidos").

Explica brevemente por qué los precios se recalculan en el backend y no se confía en los del frontend.
```

### 2.2 Views y URLs

```
Fase 2.2 — Views y enrutamiento de la API.

Crea las vistas usando ViewSets de DRF donde sea posible:

catalog/views.py:
- CategoryViewSet (solo lectura, ReadOnlyModelViewSet) con filtro por "activo=True".
- ProductViewSet (solo lectura) con: filtro por categoría vía query param (?categoria=slug), búsqueda por nombre (?search=), filtro de destacados (?destacado=true), y que use ProductListSerializer en list() y ProductDetailSerializer en retrieve().
- ComboViewSet (solo lectura).

orders/views.py:
- OrderCreateAPIView (APIView o CreateAPIView) para crear un pedido (público, sin requerir autenticación, pero si el usuario está autenticado lo asocia automáticamente).
- OrderDetailAPIView para consultar el estado de un pedido por id (protegido: solo el dueño del pedido o un pedido reciente por sesión de invitado).
- MyOrdersListAPIView (requiere autenticación) que devuelve el historial de pedidos del usuario logueado.
- Endpoint simple ValidateCouponAPIView que reciba un código de cupón y devuelva si es válido y su descuento, sin necesidad de crear el pedido (para mostrar el descuento en el carrito antes de confirmar).

delivery/views.py:
- DeliveryZoneViewSet (solo lectura) para poblar el selector de distrito en el checkout.

accounts/views.py:
- RegisterAPIView, y endpoints de login/refresh usando TokenObtainPairView y TokenRefreshView de simplejwt.
- AddressViewSet (CRUD completo, solo direcciones del usuario autenticado, usando get_queryset filtrando por request.user).

Luego dame los archivos urls.py de cada app y el urls.py principal del proyecto que los incluya todos bajo el prefijo /api/, por ejemplo /api/catalog/products/, /api/orders/, /api/delivery/zones/, /api/accounts/.
```

---

## FASE 3 — Frontend: estructura del proyecto Vue

### 3.1 Setup inicial

```
Fase 3.1 — Estructura del proyecto frontend.

Genera la estructura inicial de un proyecto Vue 3 con Vite llamado "chifa-frontend", usando Composition API con <script setup>, Vue Router, Pinia, Axios y TailwindCSS.

Entrégame:
1. El árbol de carpetas propuesto, organizado así:
   src/
     assets/
     components/
       layout/
       product/
       cart/
       checkout/
     views/
     stores/
     services/
     router/
     composables/
2. package.json con las dependencias necesarias.
3. vite.config.js con alias "@" apuntando a /src y proxy de /api hacia http://localhost:8000 en desarrollo.
4. tailwind.config.js con una paleta de colores personalizada para una marca de chifa (tonos rojo/dorado, ej. primary: rojo intenso, secondary: dorado/mostaza, dark: un marrón oscuro para textos), y fuente personalizada.
5. src/services/api.js: instancia de Axios configurada con baseURL "/api", interceptor para agregar el token JWT desde el store de auth en cada request, e interceptor de respuesta para renovar el token si expira (401).
6. src/router/index.js con las rutas: Home, Menu (catálogo con filtro por categoría), ProductDetail, Cart, Checkout, OrderConfirmation (por id de pedido), MyOrders (protegida, requiere auth), Login, Register.
```

### 3.2 Stores de Pinia

```
Fase 3.2 — Stores de Pinia.

Crea los siguientes stores en src/stores/, usando la sintaxis de "setup stores" (defineStore con función, no options API):

1. useCartStore (src/stores/cart.js):
   - Estado: array de items del carrito (cada item: producto, variante seleccionada, extras seleccionados, cantidad, precio_unitario_calculado).
   - Getters: subtotal, cantidadTotalItems.
   - Acciones: agregarItem, quitarItem, actualizarCantidad, vaciarCarrito.
   - Persistencia en localStorage (guarda y restaura el carrito automáticamente con un watcher).

2. useAuthStore (src/stores/auth.js):
   - Estado: user, accessToken, refreshToken (inicializados desde localStorage si existen).
   - Acciones: login(credenciales), register(datos), logout(), fetchPerfil().
   - Getter: estaAutenticado.

3. useCatalogStore (src/stores/catalog.js):
   - Estado: categorías, productos, productoActual, cargando.
   - Acciones: fetchCategorias(), fetchProductos(filtros), fetchProductoPorSlug(slug).

Usa src/services/api.js para las llamadas HTTP. Muestra el código completo de los tres stores.
```

---

## FASE 4 — Frontend: componentes y vistas clave

### 4.1 Layout general

```
Fase 4.1 — Componentes de layout.

Crea los siguientes componentes en src/components/layout/, con estilo TailwindCSS inspirado en un sitio de delivery de comida (limpio, con acento en rojo/dorado, tarjetas con sombra suave y bordes redondeados):

1. AppHeader.vue: logo, menú de navegación (Inicio, Menú, Combos, Contacto), ícono de carrito con badge mostrando la cantidad de items (usando useCartStore), y botón de "Iniciar sesión" / avatar de usuario si está autenticado. Debe ser responsive con menú hamburguesa en móvil.
2. AppFooter.vue: horarios de atención, enlaces a redes sociales, enlace directo a WhatsApp ("¿Dudas? Escríbenos"), y datos de contacto.
3. CartDrawer.vue: panel lateral deslizante (tipo drawer) que se abre al hacer clic en el ícono del carrito, lista los items con imagen, nombre, variante, cantidad editable con botones +/-, subtotal, y un botón "Ir a pagar" que navega a /checkout.

Dame el código completo de los tres componentes, incluyendo las transiciones de Vue (<Transition>) para la apertura/cierre del CartDrawer.
```

### 4.2 Home y catálogo

```
Fase 4.2 — Vistas de Home y Menú.

1. src/views/HomeView.vue: sección hero con imagen de fondo y llamado a la acción ("Pide ahora"), fila horizontal con las categorías destacadas (cards con imagen y nombre, al hacer clic navegan a /menu?categoria=slug), y una sección "Los más pedidos" mostrando productos destacados usando el componente ProductCard.

2. src/components/product/ProductCard.vue: tarjeta de producto con imagen, nombre, descripción corta truncada, precio, botón "Agregar" que, si el producto tiene variantes o extras, abre ProductModal.vue en vez de agregarlo directo al carrito.

3. src/components/product/ProductModal.vue: modal con imagen grande, descripción completa, selector de variante (radio buttons con precio de cada una), checklist de extras con su precio adicional, selector de cantidad, cálculo de precio total en vivo, y botón "Agregar al carrito" que llama a cartStore.agregarItem() y cierra el modal.

4. src/views/MenuView.vue: barra de filtros por categoría (tabs horizontales) y grid responsive de ProductCard, consumiendo useCatalogStore.

Dame el código completo de los cuatro archivos.
```

### 4.3 Checkout

```
Fase 4.3 — Flujo de Checkout.

Crea src/views/CheckoutView.vue como un formulario de un solo paso, dividido en secciones dentro de la misma página (no wizard de múltiples pantallas), con estos bloques usando componentes hijos en src/components/checkout/:

1. DeliveryTypeSelector.vue: toggle entre "Delivery" y "Recojo en tienda".
2. DeliveryAddressForm.vue: si es delivery, muestra selector de zona/distrito (poblado desde delivery API, mostrando el costo de envío de cada uno), dirección, referencia. Si el usuario está autenticado, permite elegir entre sus direcciones guardadas o ingresar una nueva.
3. PaymentMethodSelector.vue: radio buttons para Yape/Plin (muestra un QR o número referencial estático como placeholder), Tarjeta (placeholder, sin integrar pasarela real todavía) y Efectivo contraentrega.
4. CouponInput.vue: campo para ingresar código de cupón con botón "Aplicar", que llama al endpoint de validar cupón y muestra el descuento aplicado o un mensaje de error.
5. OrderSummary.vue: resumen de items del carrito, subtotal, costo de delivery, descuento y total.

En CheckoutView.vue, arma el payload final y llama al servicio de orders para crear el pedido (POST). Al recibir respuesta exitosa, vacía el carrito y redirige a /pedido/:id/confirmacion. Maneja estados de carga y errores de validación del backend mostrando mensajes claros al usuario.

Dame el código completo de CheckoutView.vue y de los cinco componentes hijos.
```

### 4.4 Confirmación, autenticación y "Mis pedidos"

```
Fase 4.4 — Confirmación de pedido, autenticación y "Mis pedidos".

1. src/views/OrderConfirmationView.vue: obtiene el pedido por id desde la ruta, muestra número de pedido, estado actual con un indicador visual tipo timeline (Pendiente → Confirmado → En preparación → En camino → Entregado), resumen de items y total, y datos de contacto/entrega.

2. src/views/LoginView.vue y src/views/RegisterView.vue: formularios simples con validación básica (campos requeridos, formato de email), que usan useAuthStore, muestran errores del backend y redirigen al home tras éxito.

3. src/views/MyOrdersView.vue (ruta protegida): lista de pedidos pasados del usuario autenticado, cada uno como una tarjeta con fecha, total, estado y botón "Ver detalle" que navega a la vista de confirmación reutilizando el mismo componente.

4. src/router/index.js: agrega un navigation guard (beforeEach) que redirige a /login si la ruta requiere autenticación (meta: { requiresAuth: true }) y el usuario no está autenticado.

Dame el código completo de los archivos anteriores.
```

---

## FASE 5 — Integración, datos de prueba y despliegue

### 5.1 Datos de prueba (seed)

```
Fase 5.1 — Comando de gestión para poblar datos de prueba.

Crea un management command de Django (catalog/management/commands/seed_data.py) que pueble la base de datos con datos de ejemplo realistas de un chifa:
- Al menos 6 categorías (Entradas, Sopas, Arroces Chaufa, Tallarines Saltados, Wantanes, Bebidas, Postres).
- Al menos 3 productos por categoría, con nombres típicos de comida chifa peruana (ej. "Arroz Chaufa Especial", "Tallarín Saltado de Pollo", "Sopa Wantán", "Wantán Frito x6"), precios coherentes en soles (S/), y algunas con variantes de tamaño.
- 2 combos que agrupen varios productos con descuento.
- 3 zonas de delivery con distintos costos.
- Un cupón de ejemplo activo.

El comando debe poder ejecutarse con "python manage.py seed_data" y ser idempotente (no duplicar datos si se ejecuta más de una vez, usando get_or_create).
```

### 5.2 Documentación y despliegue

```
Fase 5.2 — README y guía de despliegue.

Redáctame un README.md completo para el repositorio raíz del proyecto (que contiene las carpetas /backend y /frontend), que incluya:
1. Descripción breve del proyecto.
2. Requisitos previos (Python, Node, PostgreSQL).
3. Pasos para levantar el backend en local (entorno virtual, instalar requirements, migraciones, seed_data, runserver).
4. Pasos para levantar el frontend en local (npm install, npm run dev).
5. Variables de entorno necesarias en cada lado (.env de backend y .env de frontend con VITE_API_URL).
6. Notas de despliegue en producción: backend con Gunicorn + Nginx (o alternativa como Railway/Render), frontend compilado con "npm run build" servido como estático (o en Vercel/Netlify), y recordatorio de configurar CORS y ALLOWED_HOSTS correctamente en producción.
7. Estructura de carpetas final del proyecto completo (backend + frontend).

No es necesario escribir código en este prompt, solo el contenido en Markdown del README.
```

---

## Notas de uso

- Envía los prompts en el orden numerado; DeepSeek necesita el contexto de las fases anteriores para mantener nombres de modelos y endpoints consistentes.
- Si en algún momento DeepSeek genera código inconsistente con una fase anterior (por ejemplo, nombres de campos distintos), pégale de vuelta el fragmento anterior relevante y pídele que lo ajuste antes de seguir.
- Los prompts de pago (Yape/Plin, tarjeta) están definidos como placeholders visuales a propósito: integrar una pasarela real (Culqi, Niubiz, Mercado Pago) requiere credenciales y un flujo de prompts aparte una vez tengas cuenta de comercio.
- Puedes añadir una "Fase 6" para PWA/notificaciones o para un panel propio de administración en Vue (en vez de usar solo Django Admin) si el proyecto lo requiere más adelante.
