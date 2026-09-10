from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import DeliveryZone


class DeliveryZoneTest(TestCase):
    def test_gratis_si_supera_free_over(self):
        z = DeliveryZone(name='Cercado', cost=Decimal('5.00'), free_over=Decimal('60.00'))
        self.assertEqual(z.get_delivery_cost(Decimal('10')), Decimal('5.00'))
        self.assertEqual(z.get_delivery_cost(Decimal('100')), Decimal('0'))

    def test_sin_free_over_siempre_cobra(self):
        z = DeliveryZone(name='Ate', cost=Decimal('8.00'), free_over=None)
        self.assertEqual(z.get_delivery_cost(Decimal('1000')), Decimal('8.00'))

    def test_free_menor_que_costo_invalido(self):
        z = DeliveryZone(name='X', cost=Decimal('5.00'), free_over=Decimal('2.00'))
        with self.assertRaises(ValidationError):
            z.full_clean()
