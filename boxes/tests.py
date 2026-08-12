from django.test import TestCase, Client
from django.urls import reverse
import json

from .models import Box, Product
from .packing import Packer, Item, pack_order_into_box

class PackingAlgorithmTests(TestCase):


    def setUp(self):
        self.box_10x10x10 = Box.objects.create(
            name="10 Cube", length=10, width=10, height=10, max_weight=100, cost=5.00
        )
        self.box_small = Box.objects.create(
            name="Small Box", length=5, width=5, height=5, max_weight=10, cost=2.00
        )

    def test_single_item_exact_fit(self):
        packer = Packer(10, 10, 10)
        item = Item(10, 10, 10)
        self.assertTrue(packer.pack_item(item))
        self.assertEqual(len(packer.spaces), 0) # No space left

    def test_item_too_large(self):
        packer = Packer(10, 10, 10)
        item = Item(11, 10, 10)
        self.assertFalse(packer.pack_item(item))

    def test_item_fits_with_rotation(self):
        # Space is 10x5x5, Item is 5x10x5 (needs rotation)
        packer = Packer(10, 5, 5)
        item = Item(5, 10, 5)
        self.assertTrue(packer.pack_item(item))

    def test_wasted_corner_scenario(self):
        # This tests the scenario where a large item takes up 90% of a box,
        # leaving long thin slivers of empty space that cannot fit a cube.
        packer = Packer(10, 10, 10) # Volume 1000
        item1 = Item(10, 9, 9)     # Volume 810
        item2 = Item(5, 5, 5)      # Volume 125

        self.assertTrue(packer.pack_item(item1))
        # Total volume is 935 < 1000, but physics prevents item2 from fitting
        self.assertFalse(packer.pack_item(item2))

    def test_gridlock_scenario(self):
        # This tests packing multiple items where mathematical volume passes,
        # but physical arrangement fails.
        packer = Packer(10, 10, 10) # Volume 1000

        # 4 cubes of 6x6x6 (Volume 216 each, Total 864)
        # Only ONE 6x6x6 cube can fit in a 10x10x10 box.
        cube = Item(6, 6, 6)

        self.assertTrue(packer.pack_item(cube)) # First one fits
        self.assertFalse(packer.pack_item(cube)) # Second one fails

    def test_three_way_split_creates_correct_spaces(self):
        packer = Packer(10, 10, 10)
        item = Item(5, 5, 5)

        self.assertTrue(packer.pack_item(item))
        # Should create 3 new spaces:
        # 1. Top: 5x5x5
        # 2. Right: 5x10x5
        # 3. Front: 10x10x5
        self.assertEqual(len(packer.spaces), 3)

        # Verify the volumes of the created spaces to ensure dimensions are correct
        volumes = sorted([s.width * s.height * s.length for s in packer.spaces])
        self.assertEqual(volumes, [125, 250, 500])

    def test_pack_order_into_box_weight_limit(self):
        # Items are tiny but heavy
        p1 = Product(name="Lead Weight", length=1, width=1, height=1, weight=15)

        # Will fit dimensionally, but fail weight
        self.assertFalse(pack_order_into_box(self.box_small, [p1]))

        # Fits both dimensionally and weight in the larger box
        self.assertTrue(pack_order_into_box(self.box_10x10x10, [p1]))

    def test_pack_order_into_box_success(self):
        p1 = Product(name="Item 1", length=5, width=5, height=5, weight=2)
        p2 = Product(name="Item 2", length=5, width=5, height=5, weight=2)
        p3 = Product(name="Item 3", length=10, width=5, height=5, weight=2)

        # Total weight: 6 (passes 100 max)
        # Total arrangement: Can fit side-by-side or stacked in 10x10x10
        self.assertTrue(pack_order_into_box(self.box_10x10x10, [p1, p2, p3]))

class RecommendBoxAPITests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('recommend_box')

        self.box_cheap = Box.objects.create(name="Cheap Box", length=5, width=5, height=5, max_weight=5, cost=1.00)
        self.box_expensive = Box.objects.create(name="Expensive Box", length=10, width=10, height=10, max_weight=50, cost=5.00)

        self.prod_small = Product.objects.create(name="Small Item", length=2, width=2, height=2, weight=1)
        self.prod_heavy = Product.objects.create(name="Heavy Item", length=2, width=2, height=2, weight=10)
        self.prod_long = Product.objects.create(name="Long Item", length=8, width=2, height=2, weight=1)

    def test_recommend_box_success_cheap(self):
        # Fits in both boxes, should pick the cheap one
        payload = {"product_ids": [self.prod_small.id]}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['recommended_box_id'], self.box_cheap.id)
        self.assertEqual(data['cost'], '1.00')

    def test_recommend_box_weight_forces_upgrade(self):
        # Small dimensionally, but heavy. Fails cheap box weight limit.
        payload = {"product_ids": [self.prod_heavy.id]}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['recommended_box_id'], self.box_expensive.id)

    def test_recommend_box_dimensions_force_upgrade(self):
        # Light weight, but too long for cheap box.
        payload = {"product_ids": [self.prod_long.id]}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recommended_box_id'], self.box_expensive.id)

    def test_recommend_box_fails(self):
        # Order is too large for the biggest box in the DB (Total weight: 50+, max weight is 50)
        # Using 6 heavy items to guarantee failure by weight. 6 * 10kg = 60kg. Max box is 50kg.
        payload = {"product_ids": [self.prod_heavy.id] * 6}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "No available box can fit this order.")

    def test_invalid_payloads(self):
        # Empty payload
        response = self.client.post(self.url, data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Invalid JSON
        response = self.client.post(self.url, data="invalid json", content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Missing Product ID
        response = self.client.post(self.url, data=json.dumps({"product_ids": [9999]}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
