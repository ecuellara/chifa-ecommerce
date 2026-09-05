📘 Guía de construcción paso a paso para tu E-commerce Chifa (Vue 3 + Django)
Objetivo: Construir una plantilla funcional de e-commerce para un restaurante de comida chifa, con backend Django REST API y frontend Vue 3 SPA, siguiendo las especificaciones funcionales del proyecto. Esta guía está diseñada para que tú escribas el código, tomes decisiones y aprendas en el proceso. No se proporciona código completo, sino instrucciones detalladas, explicaciones y fragmentos clave.

Metodología: Avanzarás en fases. Cada fase tiene una lista de tareas concretas. Al final de cada tarea, se sugiere cómo verificar que funciona. Si te atascas, se incluyen pistas y enlaces a documentación.

Requisitos previos:

Conocimientos básicos de Python, Django, JavaScript, Vue 3 (Composition API), HTML/CSS (Tailwind).

Tener instalado: Python 3.11+, Node.js 18+, PostgreSQL (o SQLite para desarrollo), Git, un editor de código (VS Code recomendado).

Familiaridad con terminal/consola.

FASE 0: Preparación del entorno y planificación
Objetivo: Configurar carpetas, entornos virtuales, instalar herramientas y entender la arquitectura general.

Tarea 0.1: Estructura de carpetas del proyecto
Crea una carpeta raíz para el proyecto, por ejemplo chifa_ecommerce. Dentro, crea dos subcarpetas: backend y frontend. También crea un archivo README.md en la raíz (lo completarás al final).

Tarea 0.2: Entorno virtual de Python (backend)
Dentro de backend, crea un entorno virtual: python -m venv venv

Actívalo: (Windows) venv\Scripts\activate, (macOS/Linux) source venv/bin/activate

Crea un archivo requirements.txt con las siguientes líneas (puedes añadir versiones específicas más adelante):

Django
djangorestframework
django-cors-headers
djangorestframework-simplejwt
Pillow
psycopg2-binary  # si usas PostgreSQL, si no, omítelo o usa sqlite
python-decouple

Instala las dependencias: pip install -r requirements.txt

Tarea 0.3: Proyecto Django inicial
Ejecuta: django-admin startproject chifa_backend . (dentro de backend)

Esto creará manage.py y la carpeta chifa_backend con settings, urls, etc.

Tarea 0.4: Configuración inicial de settings
Abre chifa_backend/settings.py y haz los siguientes cambios:

Agrega 'corsheaders' a INSTALLED_APPS.

Agrega CorsMiddleware al principio de MIDDLEWARE.

Define CORS_ALLOWED_ORIGINS = ["http://localhost:5173"] (puerto de Vite por defecto).

Configura MEDIA_URL = '/media/' y MEDIA_ROOT = BASE_DIR / 'media'.

Crea un archivo .env en la raíz de backend (junto a manage.py) para variables sensibles (usa python-decouple). Pon al menos SECRET_KEY, DEBUG=True, DB_NAME, etc. Crea un .env.example con valores de ejemplo.

Modifica DATABASES para usar SQLite por ahora (o PostgreSQL si prefieres).

Verifica que el proyecto arranca: python manage.py runserver y visita http://127.0.0.1:8000/ (deberías ver la página de bienvenida de Django).

Tarea 0.5: Inicializar frontend con Vite
En otra terminal, dentro de frontend:

npm create vite@latest . -- --template vue

Responde: nombre del proyecto chifa-frontend, framework Vue, variante JavaScript (o TypeScript si te sientes cómodo).

Instala dependencias: npm install

Instala adicionales: npm install vue-router pinia axios tailwindcss @tailwindcss/forms

Inicializa TailwindCSS: npx tailwindcss init -p (esto crea tailwind.config.js y postcss.config.js).

Configura Tailwind: en tailwind.config.js, establece content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"]. Añade una paleta de colores personalizada en theme.extend.colors (rojo, dorado, etc.).

En src/main.js, importa ./index.css (crea ese archivo y pon las directivas @tailwind base; @tailwind components; @tailwind utilities;).

Prueba que el frontend arranca: npm run dev y visita http://localhost:5173.

Verificación: Tienes un backend Django corriendo en el puerto 8000 y un frontend Vite en el 5173, ambos con configuración básica. Has definido la estructura de carpetas.

FASE 1: Backend - Modelos y admin (base)
Objetivo: Crear los modelos de datos y el panel de administración de Django.

Tarea 1.1: Crear las apps de Django
Dentro de backend, ejecuta:

python manage.py startapp core
python manage.py startapp catalog
python manage.py startapp orders
python manage.py startapp delivery
python manage.py startapp accounts

Registra estas apps en INSTALLED_APPS en settings.py.

Tarea 1.2: Modelo base TimeStampedModel
En core/models.py, define una clase abstracta TimeStampedModel con campos created_at y updated_at (DateTimeField auto_now_add y auto_now). Hereda de models.Model.

Crea también core/permissions.py (lo usarás luego para permisos personalizados). Por ahora déjalo vacío.

Tarea 1.3: Modelos de catalog
Abre catalog/models.py. Debes importar TimeStampedModel de core.models.

Define los siguientes modelos (consulta la especificación en el prompt original para los campos):

Category

Product

ProductVariant

ProductExtra

Combo (con tabla intermedia ComboItem)

Para cada modelo, agrega:

__str__

Meta con ordering

slug generado automáticamente en save() usando slugify.

Consejo: Usa ManyToManyField con through='ComboItem' para la relación entre Combo y Product.

Pista: Para ProductExtra, la relación con Product es ManyToMany, pero luego en el carrito se guardarán los extras seleccionados.

Tarea 1.4: Modelos de accounts, delivery y orders
En accounts/models.py: crea CustomUser (hereda de AbstractUser) con campo telefono (CharField). También Address con FK a usuario.

En delivery/models.py: DeliveryZone con nombre, costo, tiempo estimado, activo.

En orders/models.py: Coupon, Order (con todos los campos listados en el prompt original), y OrderItem (con FK a Order, Product, Variant nullable, y ManyToMany a ProductExtra).

Agrega el método calcular_total() en Order que sume los subtotales de los items y aplique descuento y delivery.

Agrega clean() para validar que si tipo_entrega es "delivery", dirección y zona sean obligatorios.

Tarea 1.5: Configurar AUTH_USER_MODEL
En settings.py, añade AUTH_USER_MODEL = 'accounts.CustomUser'.

Crea las migraciones: python manage.py makemigrations y python manage.py migrate. (Si usas SQLite, no hay problema; si usas PostgreSQL, asegúrate de tener las credenciales).

Tarea 1.6: Registrar modelos en Django Admin
En cada app, crea o modifica admin.py para registrar los modelos con personalizaciones:

catalog/admin.py: ProductAdmin con inlines para variantes, CategoryAdmin con list_editable para orden.

orders/admin.py: OrderAdmin con list_filter, search_fields, y un OrderItemInline (TabularInline).

accounts/admin.py: extiende UserAdmin para incluir telefono.

delivery/admin.py: registro simple.

Crea un superusuario: python manage.py createsuperuser y accede a /admin para verificar que todo está registrado.

Verificación: Desde el admin, puedes agregar categorías, productos (con variantes), zonas de delivery, etc. Prueba a crear algunos registros.

FASE 2: Backend - API REST (serializers, views, endpoints)
Objetivo: Exponer los datos mediante una API RESTful.

Tarea 2.1: Crear serializers
En catalog/serializers.py: define CategorySerializer, ProductExtraSerializer, ProductVariantSerializer, ProductListSerializer (campos reducidos), ProductDetailSerializer (anidado con variantes y extras), y ComboSerializer.

En orders/serializers.py: OrderItemSerializer, OrderCreateSerializer (con validación y creación de pedido en método create), OrderDetailSerializer.

En delivery/serializers.py: DeliveryZoneSerializer.

En accounts/serializers.py: UserSerializer, AddressSerializer.

Importante: En OrderCreateSerializer, en el método create, recalcula precios desde la base de datos (no confíes en el precio enviado). Debes obtener el producto, la variante (si existe), los extras, calcular el subtotal por item, sumar, aplicar cupón si procede, y calcular delivery según zona. Todo en una transacción atómica (transaction.atomic()).

Pista: Investiga cómo usar serializers.SerializerMethodField y validate methods.

Tarea 2.2: Crear views (ViewSets o APIViews)
En catalog/views.py: CategoryViewSet (ReadOnlyModelViewSet) y ProductViewSet (ReadOnly, con filtros por categoría, búsqueda, destacados). Usa get_queryset y get_serializer_class según el método (list usa ProductListSerializer, retrieve usa ProductDetailSerializer).

En orders/views.py: OrderCreateAPIView (público), OrderDetailAPIView (con permisos: solo el dueño), MyOrdersListAPIView (requiere autenticación), ValidateCouponAPIView (público).

En delivery/views.py: DeliveryZoneViewSet (ReadOnly).

En accounts/views.py: RegisterAPIView (creación de usuario), y usa TokenObtainPairView y TokenRefreshView de simplejwt para login/refresh. También AddressViewSet con permisos de autenticación y filtro por usuario.

Pista: Usa permission_classes y authentication_classes según corresponda.

Tarea 2.3: Configurar URLs
Crea urls.py en cada app y conéctalos desde el urls.py principal bajo el prefijo /api/. Por ejemplo:

/api/catalog/ (incluye routers para Category y Product)

/api/orders/ (para crear pedido, detalle, mis pedidos, validar cupón)

/api/delivery/ (zonas)

/api/accounts/ (registro, login, refresh, addresses)

Asegúrate de incluir el router de DRF para los ViewSets.

Tarea 2.4: Probar la API con Postman o el navegador
Arranca el servidor (python manage.py runserver).

Prueba los endpoints:

GET /api/catalog/categories/

GET /api/catalog/products/?categoria=entradas

POST /api/accounts/register/ con datos de usuario.

POST /api/accounts/login/ con credenciales (devuelve access y refresh).

POST /api/orders/order-create/ con un payload de ejemplo para crear un pedido.

Verifica que los permisos funcionen (ej. no puedas ver pedidos de otros).

Verificación: Tienes una API funcional con autenticación JWT, que permite listar productos, crear pedidos, registrar usuarios, etc. Documenta los endpoints en un archivo API.md para referencia futura.

FASE 3: Frontend - Estructura, stores y servicios
Objetivo: Configurar el frontend Vue 3 con enrutamiento, gestión de estado (Pinia) y comunicación con la API.

Tarea 3.1: Estructura de carpetas
Dentro de src crea: assets/, components/ (con subcarpetas layout/, product/, cart/, checkout/, admin/ más adelante), views/, stores/, services/, router/, composables/.

Crea src/services/api.js: configura Axios con baseURL (/api o VITE_API_URL), interceptores para añadir el token JWT (obtenido del store de auth) y manejo de errores (refrescar token si expira).

Crea un archivo .env en frontend con VITE_API_URL=http://localhost:8000/api (o /api con proxy).

Tarea 3.2: Configurar Vue Router
En src/router/index.js, define las rutas iniciales:

/ → HomeView

/menu → MenuView

/product/:slug → ProductDetailView (o usar modal, tú decides)

/cart → CartView (o drawer, pero tendrás una vista para el checkout)

/checkout → CheckoutView

/order/:id/confirmation → OrderConfirmationView

/my-orders → MyOrdersView (protegida)

/login → LoginView

/register → RegisterView

Agrega un navigation guard (beforeEach) que verifique meta: { requiresAuth: true } y redirija a login si no hay token.

Tarea 3.3: Crear los stores de Pinia (setup stores)
useAuthStore: maneja user, accessToken, refreshToken (guardados en localStorage). Acciones: login, register, logout, fetchPerfil.

useCartStore: estado items (array con producto, variante, extras, cantidad, precio_unitario). Getters: subtotal, totalItems. Acciones: agregarItem, quitarItem, actualizarCantidad, vaciarCarrito. Persistencia en localStorage con watch o usando pinia-plugin-persistedstate (puedes instalar este plugin). La lógica de agregar item debe verificar si ya existe el mismo producto+variante+extras para acumular cantidad.

useCatalogStore: estado para categorías, productos (listado), productoActual. Acciones: fetchCategorias, fetchProductos (con filtros opcionales), fetchProductoPorSlug.

Pista: En api.js, al hacer login, guarda el token en el store y en localStorage.

Tarea 3.4: Probar la conexión
En App.vue, muestra un botón que llame a catalogStore.fetchCategorias() y muestre las categorías en consola. Verifica que la API responde.

Crea un componente simple LoginForm.vue que use authStore.login y redirija al home.

FASE 4: Frontend - Componentes y vistas principales
Objetivo: Construir la interfaz de usuario: layout, home, menú, carrito lateral, modal de producto.

Tarea 4.1: Layout general
Crea AppHeader.vue: logo, menú de navegación, ícono de carrito con badge (cantidad desde cartStore), y avatar de usuario (si está autenticado) o botón "Iniciar sesión". Hazlo responsive con menú hamburguesa.

Crea AppFooter.vue: horarios, enlaces a redes sociales (solo íconos), WhatsApp, contacto.

Crea CartDrawer.vue: panel lateral que se abre/cierra con transición. Muestra los items del carrito con imagen, nombre, variante, cantidad con botones +/- y precio. Al final, subtotal y botón "Ir a pagar" (navega a checkout). Usa el store de carrito.

Verificación: Al hacer clic en el ícono del carrito, se abre el drawer con los items (puedes agregar algunos manualmente para probar). Los botones + y - actualizan cantidades y el subtotal.

Tarea 4.2: Home y catálogo
HomeView.vue: sección hero con imagen de fondo y botón "Pide ahora". Debajo, un scroll horizontal de categorías destacadas (cards con imagen y nombre, al hacer clic navega a /menu?categoria=slug). Luego, una sección "Los más pedidos" con grid de ProductCard.vue (productos destacados).

ProductCard.vue: tarjeta con imagen (usa img con fallback), nombre, descripción corta truncada, precio base. Botón "Agregar". Si el producto tiene variantes o extras, al hacer clic se abre ProductModal.vue; si no, agrega directamente al carrito (con variante por defecto y sin extras).

ProductModal.vue: modal que muestra imagen grande, descripción completa, selector de variante (radio buttons con precio), lista de extras con checkbox y precio, selector de cantidad (input number). Calcula precio total en tiempo real (precio base + variante + extras * cantidad). Botón "Agregar al carrito" que llama a cartStore.agregarItem con los datos seleccionados y cierra el modal.

MenuView.vue: barra de pestañas horizontales con las categorías (todas o solo activas), y un grid de ProductCard filtrado por la categoría seleccionada (usando query param de la URL). También permite búsqueda por nombre (puedes agregar un input de búsqueda).

Verificación: Navega a /menu, filtra por categoría, haz clic en un producto con variantes y verás el modal. Agrega al carrito y el drawer se actualiza.

FASE 5: Frontend - Checkout y confirmación
Objetivo: Implementar el flujo de compra.

Tarea 5.1: CheckoutView y componentes hijos
CheckoutView.vue: formulario de una sola página con las secciones:

DeliveryTypeSelector: toggle entre "Delivery" y "Recojo en tienda". Muestra condicionalmente el formulario de dirección.

DeliveryAddressForm: si es delivery, carga zonas de delivery desde la API (select con costo de envío), campo dirección, referencia. Si usuario autenticado, puede elegir entre direcciones guardadas (fetch de /api/accounts/addresses/). Muestra el costo de envío según zona.

PaymentMethodSelector: radio buttons para Yape/Plin (muestra imagen QR o número de referencia), Tarjeta (placeholder) y Efectivo.

CouponInput: input y botón "Aplicar" que valida el cupón mediante ValidateCouponAPIView y actualiza el descuento en el resumen.

OrderSummary: resumen de items del carrito (con imagen, nombre, cantidad, precio unitario), subtotal, delivery, descuento, total.

Al hacer clic en "Confirmar pedido", arma el payload según la estructura esperada por OrderCreateSerializer (items, datos de contacto, tipo entrega, dirección, método pago, cupón, comentarios). Llama a api.post('/orders/order-create/', payload). En caso de éxito, vacía el carrito, guarda el id del pedido y redirige a /order/:id/confirmation. Maneja errores (mostrar mensajes debajo de cada campo).

Tarea 5.2: OrderConfirmationView
Obtiene el pedido por id desde la ruta (usando useRoute). Llama a api.get(/orders/order/${id}/) para obtener los detalles.

Muestra número de pedido, estado actual con una línea de tiempo (Pendiente → Confirmado → En preparación → En camino → Entregado) con círculos de colores.

Resumen de items, total, datos de entrega/contacto.

Botón "Volver al inicio".

Tarea 5.3: Login y Register
Crea vistas LoginView.vue y RegisterView.vue con formularios que usan useAuthStore. Después de login/register, redirige a la página anterior o al home.

Tarea 5.4: MyOrdersView (protegida)
Muestra lista de pedidos del usuario (desde api.get('/orders/my-orders/')). Cada pedido se muestra en una tarjeta con fecha, total, estado y un botón "Ver detalle" que navega a OrderConfirmationView con ese id.

Verificación: Realiza un flujo de compra completo: agrega productos al carrito, ve al checkout, completa los datos (elige delivery, dirección, método de pago), aplica un cupón de prueba, confirma, y al final ves la página de confirmación. Luego inicia sesión y verifica que el pedido aparece en "Mis pedidos".

FASE 6: Datos de prueba y administración Django
Tarea 6.1: Crear comando de seed
En catalog/management/commands/seed_data.py, escribe un comando que cree datos de ejemplo usando get_or_create (para ser idempotente). Incluye categorías, productos con variantes, combos, zonas de delivery, un cupón de prueba. Ejecuta python manage.py seed_data para poblar la BD.

Tarea 6.2: README.md
Redacta un README.md en la raíz del proyecto con instrucciones de instalación y ejecución tanto para backend como frontend, variables de entorno, y notas de despliegue (Gunicorn/Nginx, Vercel/Netlify). Incluye el árbol de carpetas final.

FASE 7 (Opcional): Panel de administración propio en Vue (staff)
Si quieres añadir un panel para el restaurante, sigue estos pasos, que son extensiones del proyecto actual.

Tarea 7.1: Backend - permisos y endpoints staff
En accounts/models.py, añade un campo booleano is_restaurant_staff (o usa grupos). Crea un permiso personalizado IsRestaurantStaff.

Agrega endpoints en orders/views.py: AdminOrderListAPIView (listar todos los pedidos con filtros), AdminOrderUpdateStatusAPIView (PATCH para cambiar estado), AdminDashboardStatsAPIView (métricas del día).

En catalog/views.py, crea AdminProductViewSet, AdminCategoryViewSet, AdminComboViewSet con operaciones CRUD completas, protegidos con IsRestaurantStaff.

Actualiza las URLs bajo /api/admin-panel/.

Tarea 7.2: Frontend - layout y autenticación staff
Crea AdminLoginView.vue (similar a login pero con verificación de rol).

Crea AdminLayout.vue con sidebar fijo y header.

En el router, agrega rutas hijas bajo /panel con meta: { requiresStaff: true } y un guard que redirija a /panel/login si no es staff.

Tarea 7.3: Dashboard y gestión de pedidos
DashboardView.vue: tarjetas de métricas y tabla de últimos pedidos.

OrdersManagementView.vue: tabla con filtros por estado, selector de cambio de estado en cada fila, y modal/drawer de detalle. Implementa polling cada 30 segundos para actualizar.

Tarea 7.4: CRUD de catálogo
Crea vistas para gestionar productos (con formulario para variantes y extras), categorías, combos, cupones y zonas de delivery. Usa componentes reutilizables para listados y formularios en modal.

📌 Consejos generales para el desarrollo
Control de versiones: Haz commits frecuentes después de cada tarea completada.

Depuración: Usa print() o logging en backend; en frontend usa console.log y Vue Devtools.

Validación de datos: Siempre valida en el backend (no confíes en el frontend). Usa serializers con validate y validators.

Seguridad: No expongas secretos; usa variables de entorno.

Estilo: Sigue las convenciones de Django y Vue. Usa composables para lógica reutilizable.

Pruebas: Escribe pruebas unitarias para modelos y vistas (puedes dejarlo para el final).

Documentación: Comenta el código donde sea necesario, pero prioriza nombres claros.

Recursos recomendados:

Documentación oficial de Django: https://docs.djangoproject.com/

DRF: https://www.django-rest-framework.org/

Vue 3: https://vuejs.org/guide/introduction.html

Pinia: https://pinia.vuejs.org/

TailwindCSS: https://tailwindcss.com/docs

🚀 Próximos pasos (si quieres extender)
Integración real de pagos (Culqi, MercadoPago).

WebSockets para actualización en tiempo real de pedidos.

Notificaciones por correo/SMS al crear pedido.

Sistema de reseñas y calificaciones.

Internacionalización (i18n).

¡Adelante! Tómate tu tiempo, y si tienes dudas, busca en la documentación o foros. El objetivo es que entiendas cada parte del sistema. ¡Buena suerte!