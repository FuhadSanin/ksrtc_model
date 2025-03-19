import json
import os
import django

# ✅ Set up Django before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ksrtc_model.settings")  # Update with your actual project name
django.setup()

from django.contrib.auth.models import User
from ksrtc.models import BusTrip


def import_data():
    file_path = os.path.join(os.path.dirname(__file__), "json", "kozhikode.json")

    if not os.path.exists(file_path):
        print(f"❌ Error: JSON file not found at {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ Get an existing user (Change logic if necessary)
    user = User.objects.filter(id=3).first()
    if not user:
        print("❌ No user found. Create one with `python manage.py createsuperuser`")
        return

    for index, trip in enumerate(data, start=1):
        vehicle_number = trip["vehicle_number"]
        stations = trip["stations"]

        bus_trip, created = BusTrip.objects.update_or_create(
            vehicle_number=vehicle_number,
            defaults={"trip": index, "stations": stations, "user": user},
        )

        status = "Created" if created else "Updated"
        print(f"✅ {status}: {bus_trip}")

    print("🚀 Import completed!")


if __name__ == "__main__":
    import_data()