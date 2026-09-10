from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from catalog.models import Category, Product
from delivery.models import DeliveryZone
from .models import Order


def make_catalog():
    cat = Category.objects.create(name='Chaufas', slug='chaufas')
    p = Product.objects.create(category=cat, name='Chaufa', slug='chaufa', price=Decimal('25.50'))
    z = DeliveryZone.objects.create(name='Cercado', cost=Decimal('5.00'), free_over=Decimal('60.00'))
    return cat, p, z


class OrderCreateTest(TestCase):
    def setUp(self):
        _, self.p, self.z = make_catalog()
        self.client = APIClient()

    def test_recalcula_precio_y_delivery(self):
        r = self.client.post('/api/orders/', {
            'tipo_entrega': 'delivery', 'nombre': 'Juan', 'telefono': '999',
            'zona_id': self.z.id, 'direccion': 'Av 123', 'metodo_pago': 'efectivo',
            'items': [{'product_id': self.p.id, 'qty': 2}],
        }, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(str(r.data['subtotal']), '51.00')
        self.assertEqual(str(r.data['delivery_cost']), '5.00')
        self.assertEqual(str(r.data['total']), '56.00')

    def test_gratis_si_supera_umbral(self):
        r = self.client.post('/api/orders/', {
            'tipo_entrega': 'delivery', 'nombre': 'Juan', 'telefono': '999',
            'zona_id': self.z.id, 'direccion': 'Av 123', 'metodo_pago': 'efectivo',
            'items': [{'product_id': self.p.id, 'qty': 3}],
        }, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(str(r.data['delivery_cost']), '0.00')

    def test_producto_inactivo_bloqueado(self):
        self.p.is_active = False
        self.p.save()
        r = self.client.post('/api/orders/', {
            'tipo_entrega': 'recojo', 'nombre': 'Juan', 'telefono': '999',
            'metodo_pago': 'efectivo',
            'items': [{'product_id': self.p.id, 'qty': 1}],
        }, format='json')
        self.assertEqual(r.status_code, 400)

    def test_transicion_invalida_bloqueada(self):
        o = Order.objects.create(tipo_entrega='recojo', nombre='A', telefono='1',
                                 subtotal=10, total=10, estado='pendiente')
        o.estado = 'entregado'
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            o.full_clean()

    def test_track_exige_telefono(self):
        o = Order.objects.create(tipo_entrega='recojo', nombre='A', telefono='999',
                                 subtotal=10, total=10)
        self.assertEqual(self.client.get(f'/api/orders/track/?id={o.id}&telefono=000').status_code, 404)
        self.assertEqual(self.client.get(f'/api/orders/track/?id={o.id}&telefono=999').status_code, 200)


class StaffPermTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cli = User.objects.create_user(username='cli', password='x12345678')
        self.staff = User.objects.create_user(username='boss', password='x12345678', is_staff=True)

    def test_staff_endpoints_seguridad(self):
        self.assertEqual(self.client.get('/api/staff/stats/').status_code, 401)
        self.client.force_authenticate(user=self.cli)
        self.assertEqual(self.client.get('/api/staff/stats/').status_code, 403)
        self.client.force_authenticate(user=self.staff)
        self.assertEqual(self.client.get('/api/staff/stats/').status_code, 200)
