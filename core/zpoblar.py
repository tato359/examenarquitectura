import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='carlos',
        tipo='Cliente', 
        nombre='carlos', 
        apellido='carrillo', 
        correo=test_user_email if test_user_email else 'carlos@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/user6.png')

    crear_usuario(
        username='joa',
        tipo='Cliente', 
        nombre='joaquin', 
        apellido='lagos', 
        correo=test_user_email if test_user_email else 'joaquin@marvels.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/user4.png')

    crear_usuario(
        username='eme',
        tipo='Cliente', 
        nombre='Emerson', 
        apellido='Lemunao', 
        correo=test_user_email if test_user_email else 'emerson@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user2.jpg')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson', 
        correo=test_user_email if test_user_email else 'sjohansson@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user7.jpg')

    crear_usuario(
        username='marcelo',
        tipo='Administrador', 
        nombre='marcelo', 
        apellido='delchuce', 
        correo=test_user_email if test_user_email else 'delchuce@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user3.jpg')
    
    crear_usuario(
        username='tauro',
        tipo='Administrador', 
        nombre='alde', 
        apellido='baran', 
        correo=test_user_email if test_user_email else 'aldebaran@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user5.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='clark',
        apellido='kent',
        correo=test_user_email if test_user_email else 'superman@gmail.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/user1.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Teclado'},
        { 'id': 2, 'nombre': 'Mouse'},
        { 'id': 3, 'nombre': 'Monitor'},
        { 'id': 4, 'nombre': 'Auriculares'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
           
    #Categoría "Teclados" (4 productos)
     {
       'id': 1,
        'categoria': Categoria.objects.get(id=1),
       'nombre': 'Teclado Mecánico HyperX Alloy FPS Pro',
        'descripcion': 'Teclado mecánico compacto diseñado para jugadores profesionales, con interruptores Cherry MX y retroiluminación LED roja.',
       'precio': 49990,
    'descuento_subscriptor': 10,
    'descuento_oferta': 15,
    'imagen': 'productos/teclado_hyperx.jpg'
      },
     {
         'id': 2,
         'categoria': Categoria.objects.get(id=1),
         'nombre': 'Teclado Logitech K380',
         'descripcion': 'Teclado inalámbrico compacto con conectividad Bluetooth, compatible con múltiples dispositivos y diseño ergonómico.',
         'precio': 29990,
         'descuento_subscriptor': 5,
         'descuento_oferta': 10,
         'imagen': 'productos/teclado_logitech.png'
     },
    # Categoría "Mouses" (4 productos)
    {
        'id': 3,
        'categoria': Categoria.objects.get(id=2),
        'nombre': 'Mouse Gamer Razer DeathAdder V2',
        'descripcion': 'Mouse ergonómico con sensor óptico de 20,000 DPI, switches ópticos y diseño para largas sesiones de juego.',
        'precio': 49990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 20,
        'imagen': 'productos/mouse_razer.jpg'
    },
     {
         'id': 4,
         'categoria': Categoria.objects.get(id=2),
         'nombre': 'Mouse Logitech MX Master 3',
         'descripcion': 'Mouse inalámbrico avanzado para productividad, con diseño ergonómico, múltiples botones personalizables y rueda de desplazamiento precisa.',
         'precio': 79990,
         'descuento_subscriptor': 10,
         'descuento_oferta': 15,
         'imagen': 'productos/teclado_logitech.jpg'
     },
    # # Categoría "Monitores" (4 productos)
     {
         'id': 5,
         'categoria': Categoria.objects.get(id=3),
         'nombre': 'Monitor LG UltraGear 27GL83A',
         'descripcion': 'Monitor de 27 pulgadas con resolución QHD, tasa de refresco de 144Hz y soporte para G-Sync para una experiencia de juego fluida.',
         'precio': 259990,
         'descuento_subscriptor': 10,
         'descuento_oferta': 20,
         'imagen': 'productos/monitor_lg.jpg'
    },
     {
         'id': 6,
         'categoria': Categoria.objects.get(id=3),
         'nombre': 'Monitor Dell UltraSharp U2723QE',
         'descripcion': 'Monitor 4K Ultra HD con tecnología IPS Black, ideal para trabajos de diseño y edición profesional.',
         'precio': 379990,
         'descuento_subscriptor': 15,
         'descuento_oferta': 10,
         'imagen': 'productos/monitor_dell.png'
     },
    # # Categoría "Audífonos" (4 productos)
     {
         'id': 7,
         'categoria': Categoria.objects.get(id=4),
         'nombre': 'Audífonos Sony WH-1000XM5',
         'descripcion': 'Audífonos inalámbricos con cancelación activa de ruido líder en el mercado, diseño cómodo y sonido premium.',
         'precio': 299990,
         'descuento_subscriptor': 15,
         'descuento_oferta': 10,
         'imagen': 'productos/audifonos_sony.png'
     },
     {
         'id': 8,
         'categoria': Categoria.objects.get(id=4),
         'nombre': 'Audífonos HyperX Cloud II',
         'descripcion': 'Audífonos gamer con sonido envolvente 7.1, micrófono desmontable y almohadillas cómodas para largas sesiones de uso.',
         'precio': 99990,
         'descuento_subscriptor': 10,
         'descuento_oferta': 15,
         'imagen': 'productos/audifonos_hyperx.jpg'
     },
    {
        'id': 9,
        'categoria': Categoria.objects.get(id=3),  # Monitor
        'nombre': 'Monitor ASUS TUF Gaming VG259Q',
        'descripcion': 'Monitor de 24.5" Full HD con panel IPS, frecuencia de actualización de 144Hz y tecnología G-SYNC compatible para experiencias de juego fluidas.',
        'precio': 199990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 20,
        'imagen': 'productos/monitor_asus_tuf.jpg'
    },
    {
        'id': 10,
        'categoria': Categoria.objects.get(id=3),  # Monitor
        'nombre': 'Monitor Samsung Odyssey G5',
        'descripcion': 'Monitor curvo de 27" con resolución QHD, frecuencia de 144Hz y soporte HDR10 para juegos inmersivos.',
        'precio': 249990,
        'descuento_subscriptor': 15,
        'descuento_oferta': 25,
        'imagen': 'productos/monitor_samsung_odyssey.jpg'
    },
    {
        'id': 11,
        'categoria': Categoria.objects.get(id=4),  # Audífonos
        'nombre': 'Audífonos HyperX Cloud II',
        'descripcion': 'Audífonos gaming con sonido envolvente 7.1 virtual, almohadillas de memory foam y micrófono desmontable.',
        'precio': 89990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 10,
        'imagen': 'productos/audifonos_hyperx_cloud2.jpg'
    },
    {
        'id': 12,
        'categoria': Categoria.objects.get(id=2),  # Mouse
        'nombre': 'Mouse Logitech G502 HERO',
        'descripcion': 'Mouse gaming con sensor HERO 25K, 11 botones programables y sistema de pesas ajustables.',
        'precio': 59990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 15,
        'imagen': 'productos/mouse_logitech_g502.jpg'
    },
    {
        'id': 13,
        'categoria': Categoria.objects.get(id=3),  # Monitor
        'nombre': 'Monitor LG UltraGear 24GN600',
        'descripcion': 'Monitor de 24" con panel IPS, resolución Full HD, 144Hz y tiempo de respuesta de 1ms para juegos de alta velocidad.',
        'precio': 179990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 15,
        'imagen': 'productos/monitor_lg_ultragear.jpg'
    },   
]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')
    
    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')



