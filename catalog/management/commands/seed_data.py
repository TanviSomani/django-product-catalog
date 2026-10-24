from django.core.management.base import BaseCommand
from catalog.models import Category, Product, Tag


class Command(BaseCommand):
    help = "Add example categories, tags, and products for trying out the catalog."

    def handle(self, *args, **options):
        category_details = {
            "Electronics": "Everyday electronic devices and accessories.",
            "Home": "Useful items for living spaces.",
            "Kitchen": "Tools and accessories for food preparation.",
            "Outdoor": "Gear for trips and outdoor activities.",
            "Office": "Supplies and equipment for work or study.",
        }
        categories = {}
        for name, description in category_details.items():
            categories[name], _ = Category.objects.get_or_create(
                name=name, defaults={"description": description}
            )

        tag_names = [
            "Wireless", "Travel", "Eco-friendly", "Lightweight", "Premium",
            "Budget", "New Arrival", "Bestseller", "Compact", "Rechargeable",
        ]
        tags = {}
        for name in tag_names:
            tags[name], _ = Tag.objects.get_or_create(name=name)

        sample_products = [
            ("Wireless Headphones", "Wireless headphones with comfortable ear cushions for travel.", "Electronics", ["Wireless", "Travel", "Bestseller"]),
            ("Portable Speaker", "A compact wireless speaker for music at home or outdoors.", "Electronics", ["Wireless", "Compact", "Rechargeable"]),
            ("USB-C Hub", "A lightweight USB-C hub with extra ports for laptops.", "Electronics", ["Lightweight", "Compact", "Budget"]),
            ("Desk Lamp", "An adjustable desk lamp with a rechargeable battery.", "Office", ["Rechargeable", "Compact"]),
            ("Laptop Stand", "A lightweight laptop stand that keeps a desk organized.", "Office", ["Lightweight", "Premium"]),
            ("Notebook Set", "A set of recycled paper notebooks for work and study.", "Office", ["Eco-friendly", "Budget", "Bestseller"]),
            ("Insulated Bottle", "A reusable insulated bottle for daily use and travel.", "Outdoor", ["Eco-friendly", "Travel", "Bestseller"]),
            ("Daypack", "A compact daypack with room for essentials on short trips.", "Outdoor", ["Travel", "Compact", "New Arrival"]),
            ("Camping Lantern", "A rechargeable lantern for campsites and evening walks.", "Outdoor", ["Rechargeable", "Travel"]),
            ("Travel Mug", "A lightweight travel mug designed to keep drinks warm.", "Kitchen", ["Travel", "Lightweight", "Budget"]),
            ("Ceramic Mug", "A sturdy ceramic mug for coffee or tea at home.", "Kitchen", ["Budget", "Bestseller"]),
            ("Cutting Board", "A durable cutting board made with responsibly sourced wood.", "Kitchen", ["Eco-friendly", "Premium"]),
            ("Food Storage Set", "Reusable food containers for lunches and leftovers.", "Kitchen", ["Eco-friendly", "Compact", "New Arrival"]),
            ("Cotton Throw", "A soft cotton throw for a sofa, reading chair, or bed.", "Home", ["Premium", "New Arrival"]),
            ("Storage Basket", "A compact basket for keeping small household items tidy.", "Home", ["Compact", "Budget"]),
            ("LED Bulb Pack", "Energy-saving LED bulbs for everyday household lighting.", "Home", ["Eco-friendly", "Budget"]),
            ("Wireless Mouse", "A compact wireless mouse for laptops and desktop computers.", "Electronics", ["Wireless", "Compact", "Bestseller"]),
            ("Power Bank", "A portable rechargeable power bank for phones and small devices.", "Electronics", ["Rechargeable", "Travel", "New Arrival"]),
            ("Reusable Tote", "A lightweight reusable tote bag for shopping and errands.", "Home", ["Eco-friendly", "Lightweight", "Budget"]),
            ("Monitor Riser", "A sturdy monitor riser with space for desk accessories.", "Office", ["Compact", "Premium", "New Arrival"]),
        ]

        created = 0
        for name, description, category_name, product_tags in sample_products:
            product, was_created = Product.objects.get_or_create(
                name=name,
                category=categories[category_name],
                defaults={"description": description},
            )
            if not was_created and product.description != description:
                product.description = description
                product.save(update_fields=["description"])
            product.tags.set([tags[tag_name] for tag_name in product_tags])
            created += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample data ready: {Category.objects.count()} categories, "
                f"{Tag.objects.count()} tags, {Product.objects.count()} products. "
                f"Added {created} new products in this run."
            )
        )
