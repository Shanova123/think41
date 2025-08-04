import csv
import os
from django.core.management.base import BaseCommand
from ecommerce.models import User, Order
from datetime import datetime
from django.conf import settings

class Command(BaseCommand):
    help = 'Import users and orders from CSV files'

    def handle(self, *args, **kwargs):
        users_path = os.path.join(settings.BASE_DIR, 'users.csv')
        orders_path = os.path.join(settings.BASE_DIR, 'orders.csv')

        # 🔹 Import Users with bulk_create
        users = []
        try:
            with open(users_path, newline='', encoding='utf-8-sig') as users_file:
                reader = csv.DictReader(users_file)
                print("🧾 USER CSV HEADERS:", reader.fieldnames)
                for idx, row in enumerate(reader, 1):
                    try:
                        users.append(User(
                            id=int(row['user_id']),
                            first_name=row.get('first_name', ''),
                            last_name=row.get('last_name', ''),
                            email=row.get('email', ''),
                            age=int(row['age']) if row.get('age') else None,
                            gender=row.get('gender', ''),
                            state=row.get('state', ''),
                            street_address=row.get('street_address', ''),
                            postal_code=row.get('postal_code', ''),
                            city=row.get('city', ''),
                            country=row.get('country', ''),
                            latitude=float(row['latitude']) if row.get('latitude') else None,
                            longitude=float(row['longitude']) if row.get('longitude') else None,
                            traffic_source=row.get('traffic_source', ''),
                            dob=datetime.fromisoformat(row['created_at'].split("T")[0]).date()
                        ))
                        if idx % 100 == 0:
                            print(f"✅ Processed {idx} users...")
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"❌ Error parsing user {row.get('user_id', 'Unknown')}: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to open users.csv: {e}"))
            return

        User.objects.bulk_create(users, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(users)} users imported successfully"))

        # 🔹 Import Orders
        orders = []
        try:
            with open(orders_path, newline='', encoding='utf-8-sig') as orders_file:
                reader = csv.DictReader(orders_file)
                print("🧾 ORDER CSV HEADERS:", reader.fieldnames)

                for idx, row in enumerate(reader, 1):
                    try:
                        orders.append(Order(
                            id=int(row['order_id']),
                            user_id=int(row['user_id']),
                            status=row.get('status', ''),
                            gender=row.get('gender', ''),
                            created_at=datetime.fromisoformat(row['created_at'].split("T")[0]),
                            shipped_at=datetime.fromisoformat(row['shipped_at'].split("T")[0]) if row.get('shipped_at') else None,
                            returned_at=datetime.fromisoformat(row['returned_at'].split("T")[0]) if row.get('returned_at') else None,
                            delivered_at=datetime.fromisoformat(row['delivered_at'].split("T")[0]) if row.get('delivered_at') else None,
                            num_of_item=int(row['num_of_item']) if row.get('num_of_item') else 0
                        ))
                        if idx % 1000 == 0:
                            print(f"📦 Processed {idx} orders...")
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"❌ Error creating order {row.get('order_id', 'Unknown')}: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to open orders.csv: {e}"))
            return

        Order.objects.bulk_create(orders)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(orders)} orders imported successfully"))
