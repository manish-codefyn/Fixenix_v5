from django.core.management.base import BaseCommand
from bookings.models import Device, DeviceBrand, DeviceModel

class Command(BaseCommand):
    help = 'Adds multiple device models to the database'

    def handle(self, *args, **kwargs):
        # Define the device types and their models
        device_models = {
    
    'Tablet': {
              'Apple': [
                    # iPad Series
                    'iPad Pro 12.9-inch (M2)', 'iPad Pro 11-inch (M2)',
                    'iPad Air (5th Generation)', 'iPad Air (4th Generation)',
                    'iPad Mini (6th Generation)', 'iPad Mini (5th Generation)',
                    'iPad (10th Generation)', 'iPad (9th Generation)',
                    'iPad Pro 12.9-inch (M1)', 'iPad Pro 11-inch (M1)',
                    'iPad Air (3rd Generation)', 'iPad Mini 4', 'iPad Pro 9.7-inch',
                ],

            'Samsung': [
        'Samsung Galaxy Tab S9 Ultra', 'Samsung Galaxy Tab S9+', 'Samsung Galaxy Tab S9', 
        'Samsung Galaxy Tab S8 Ultra', 'Samsung Galaxy Tab S8+', 'Samsung Galaxy Tab S8',
        'Samsung Galaxy Tab A8', 'Samsung Galaxy Tab Active3', 'Samsung Galaxy Tab S7 Ultra',
        'Samsung Galaxy Tab S7+', 'Samsung Galaxy Tab S7', 'Samsung Galaxy Tab A7',
        'Samsung Galaxy Tab A7 Lite', 'Samsung Galaxy Tab E', 'Samsung Galaxy Tab 4',
        'Samsung Galaxy Tab 3', 'Samsung Galaxy View 2', 'Samsung Galaxy TabPro S',
    ]
,
        'Microsoft': [
        'Surface Pro 9', 'Surface Pro 8', 'Surface Pro X', 'Surface Go 3', 'Surface Go 2', 
        'Surface Duo 2', 'Surface Duo', 
    ],
    'Lenovo': [
        'Lenovo Tab P11', 'Lenovo Tab M10 Plus', 'Lenovo Yoga Tab 13', 'Lenovo Tab M8', 'Lenovo Tab K10', 
        'Lenovo ThinkPad X1 Tablet',
    ],
    'Huawei': [
        'Huawei MatePad Pro 12.6', 'Huawei MatePad 11', 'Huawei MediaPad T5', 'Huawei MediaPad M5', 
        'Huawei MediaPad T3', 'Huawei MediaPad X2',
    ],
    'Amazon': [
        'Fire HD 10', 'Fire HD 8', 'Fire 7', 'Fire HD 10 Kids Edition', 'Fire HD 8 Kids Edition',
    ],
    'Google': [
        'Google Pixel Slate', 'Google Pixel Tablet', 'Google Nexus 9', 
    ],
    'Asus': [
        'Asus ZenPad 3S 10', 'Asus Transformer Mini T102HA', 'Asus VivoTab Smart', 
    ],
    'Acer': [
        'Acer Iconia Tab 10', 'Acer Iconia One 8', 'Acer Chromebook Tab 10', 
    ],
    'Dell': [
        'Dell Latitude 7320 Detachable', 'Dell Venue 8 7000', 
    ],
    'Sony': [
        'Sony Xperia Z4 Tablet', 'Sony Xperia Tablet Z', 'Sony Xperia Z3 Tablet Compact',
    ],
    'HP': [
        'HP Elite x2 1012 G2', 'HP Envy x2', 'HP Spectre x2', 
    ],
    'Xiaomi': [
        'Xiaomi Mi Pad 5', 'Xiaomi Mi Pad 4', 'Xiaomi Mi Pad 3', 
    ],
    'Realme': [
        'Realme Pad', 'Realme Pad X',
    ],
    'Oppo': [
        'Oppo Pad', 'Oppo Pad Air',
    ],
    'Vivo': [
        'Vivo Pad', 
    ],
    'Nokia': [
        'Nokia T20', 
    ],
    'TCL': [
        'TCL 10 TabMax', 'TCL Tab 10s',
    ],
    'LG': [
        'LG G Pad 5', 'LG G Pad 8.0', 
    ],
    'Honor': [
        'Honor Pad 7', 'Honor Pad X6', 
    ],
    'Chuwi': [
        'Chuwi HiPad X', 'Chuwi Hi10 X', 
    ],
    'Alldocube': [
        'Alldocube iPlay 40', 'Alldocube iPlay 30', 
    ],
    'Teclast': [
        'Teclast T40 Plus', 'Teclast M40', 'Teclast T10', 
    ],
    'Panasonic': [
        'Panasonic Toughpad FZ-A2', 'Panasonic Toughbook A3',
    ],
    'Blackview': [
        'Blackview Tab 8', 'Blackview Tab 9', 
    ],
    'Microsoft Surface': [
        'Microsoft Surface Pro 7', 'Microsoft Surface Go', 'Microsoft Surface Book 3',
    ],
    'Archos': [
        'Archos 101b Oxygen', 'Archos Core 101 3G', 
    ],
    'ZTE': [
        'ZTE Axon 7', 'ZTE Blade Tab 8', 
    ],
    'Infinix': [
        'Infinix Inbook X1', 'Infinix Zero Tab', 
    ],
    'Motorola': [
        'Motorola Moto Tab G20', 'Motorola Moto Tab G70', 
    ],
    'Nothing': [
        'Nothing Phone',  # Currently, Nothing has no tablets but this might be used for future references.
    ],
    'Others': [
        'Custom Tablet Model 1', 'Custom Tablet Model 2', 
    ],
            },
  



            }

        # Get the device types from the database
        devices = Device.objects.all()

        # Prepare the list of DeviceModel objects
        models = []
        for device_type_name, brands in device_models.items():
            # Check if the device type exists
            device_type = devices.filter(name=device_type_name).first()
            if device_type:
                # For each brand, check if it exists and add the models
                for brand_name, model_names in brands.items():
                    brand = DeviceBrand.objects.filter(name=brand_name, device_type=device_type).first()
                    if brand:
                        # Add models for the brand and device type
                        for model_name in model_names:
                            models.append(DeviceModel(
                                name=model_name,
                                device_type=device_type,
                                device_brand=brand
                            ))

        # Bulk create the device models
        if models:
            DeviceModel.objects.bulk_create(models)
            self.stdout.write(self.style.SUCCESS(f'{len(models)} device models added successfully!'))
        else:
            self.stdout.write(self.style.WARNING('No models were added because no matching brands or devices were found!'))
