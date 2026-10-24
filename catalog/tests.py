from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Tag


class ProductSearchTests(TestCase):
    def setUp(self):
        self.electronics = Category.objects.create(name="Electronics")
        self.home = Category.objects.create(name="Home")
        self.travel_tag = Tag.objects.create(name="Travel")
        self.wireless_tag = Tag.objects.create(name="Wireless")

        self.headphones = Product.objects.create(
            name="Wireless Headphones",
            description="Comfortable wireless headphones for travel.",
            category=self.electronics,
        )
        self.headphones.tags.add(self.travel_tag, self.wireless_tag)

        self.mug = Product.objects.create(
            name="Ceramic Mug",
            description="A sturdy mug for coffee at home.",
            category=self.home,
        )

    def test_searches_description_without_case_sensitivity(self):
        response = self.client.get(reverse("catalog:product_list"), {"q": "TRAVEL"})
        self.assertContains(response, "Wireless Headphones")
        self.assertNotContains(response, "Ceramic Mug")

    def test_filters_by_category(self):
        response = self.client.get(
            reverse("catalog:product_list"),
            {"category": self.home.id},
        )
        self.assertContains(response, "Ceramic Mug")
        self.assertNotContains(response, "Wireless Headphones")

    def test_filters_by_tag(self):
        response = self.client.get(
            reverse("catalog:product_list"),
            {"tag": self.travel_tag.id},
        )
        self.assertContains(response, "Wireless Headphones")
        self.assertNotContains(response, "Ceramic Mug")

    def test_search_and_filters_can_be_combined(self):
        response = self.client.get(
            reverse("catalog:product_list"),
            {"q": "travel", "category": self.electronics.id, "tag": self.wireless_tag.id},
        )
        self.assertContains(response, "Wireless Headphones")
        self.assertNotContains(response, "Ceramic Mug")

    def test_no_matches_shows_empty_message(self):
        response = self.client.get(reverse("catalog:product_list"), {"q": "not-a-real-product"})
        self.assertContains(response, "No products match those options")
