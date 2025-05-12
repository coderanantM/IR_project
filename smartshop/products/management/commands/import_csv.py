import os
import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product, Category

def get_category(main, sub):
    main_cat, _ = Category.objects.get_or_create(name=main, parent=None)
    sub_cat, _ = Category.objects.get_or_create(name=sub, parent=main_cat)
    return sub_cat

def clean_price(price):
    if not price or pd.isnull(price):
        return None
    price = str(price).replace('₹', '').replace(',', '').strip()
    try:
        return float(price)
    except Exception:
        return None

class Command(BaseCommand):
    help = 'Import products from CSV, specifying main and subcategory dynamically.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV file to import')
        parser.add_argument('--main_category', type=str, required=True, help='Main category name')
        parser.add_argument('--sub_category', type=str, required=True, help='Subcategory name')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        main_cat = options['main_category']
        sub_cat = options['sub_category']
        category = get_category(main_cat, sub_cat)
        file_name = os.path.basename(csv_file).lower()

        df = pd.read_csv(csv_file)
        created, updated = 0, 0

        for _, row in df.iterrows():
            # --- SHIRTS AMAZON ---
            if file_name == 'shirts_amazon.csv':
                name = row.get('brand_shirt') or row.get('brand_name') or 'No Name'
                product_url = row.get('brand_shirt_url') or ''
                price = clean_price(row.get('brand_price'))
                price_url = row.get('brand_price_url') or ''
                delivery_date = row.get('brand_delivery_date') or ''
            # --- SHIRTS FLIPKART ---
            elif file_name == 'shirt_flipkart.csv':
                name = row.get('name_shirt_type') or row.get('name_name') or 'No Name'
                product_url = row.get('name_shirt_type_url') or ''
                price = clean_price(row.get('name_price'))
                price_url = row.get('name_price_url') or ''
                delivery_date = ''
            # --- EARPHONES AMAZON ---
            elif file_name == 'earphones.csv':
                name = row.get('name_name') or 'No Name'
                product_url = ''
                price = clean_price(row.get('name_price'))
                price_url = ''
                delivery_date = ''
            # --- EARPHONES FLIPKART ---
            elif file_name == 'earphones_flipkart.csv':
                name = row.get('name_name') or 'No Name'
                product_url = row.get('name_price_url') or ''
                price = clean_price(row.get('name_price'))
                price_url = row.get('name_price_url') or ''
                delivery_date = ''
            # --- TOPS AMAZON ---
            elif file_name == 'tops_amazon.csv':
                name = row.get('brand_type') or row.get('brand_name') or 'No Name'
                product_url = row.get('brand_type_url') or ''
                price = clean_price(row.get('brand_price'))
                price_url = row.get('brand_price_url') or ''
                delivery_date = row.get('brand_delivery_date_name') or ''
            # --- LIPSTICK AMAZON ---
            elif file_name == 'lipstick_amazon.csv':
                name = row.get('name_name') or 'No Name'
                product_url = row.get('name_url') or ''
                price = clean_price(row.get('name_price'))
                price_url = row.get('name_price_url') or ''
                delivery_date = row.get('name_delivery_date_name') or ''
            # --- LIPSTICK NYKAA ---
            elif file_name == 'lipstick_nykaa.csv':
                name = row.get('name_name') or 'No Name'
                product_url = row.get('name_url') or ''
                price = clean_price(row.get('name_price'))
                price_url = row.get('name_price_url') or ''
                delivery_date = ''
            else:
                # fallback for unknown files: try to use generic column names
                name = row.get('name') or row.get('brand_name') or row.get('brand_shirt') or row.get('brand_type') or 'No Name'
                product_url = row.get('product_url') or row.get('name_url') or row.get('brand_shirt_url') or row.get('brand_type_url') or ''
                price = clean_price(row.get('price') or row.get('name_price') or row.get('brand_price'))
                price_url = row.get('price_url') or row.get('name_price_url') or row.get('brand_price_url') or ''
                delivery_date = row.get('delivery_date') or row.get('brand_delivery_date') or row.get('brand_delivery_date_name') or ''

            image_url = row.get('image_url') or ''
            rating = row.get('rating') or row.get('name_ratings') or None
            reviews = row.get('reviews') or row.get('name_reviews') or ''
            source_site = (
                'Amazon' if 'amazon' in file_name else
                'Flipkart' if 'flipkart' in file_name else
                'Nykaa' if 'nykaa' in file_name else
                'Unknown'
            )

            obj, was_created = Product.objects.update_or_create(
                name=name,
                category=category,
                defaults={
                    'product_url': product_url,
                    'price': price,
                    'price_url': price_url,
                    'delivery_date': delivery_date,
                    'image_url': image_url,
                    'rating': rating,
                    'source_site': source_site,
                    'reviews': reviews,
                    'is_available': True,
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported {created} new and updated {updated} products into {main_cat} > {sub_cat}"
        ))
