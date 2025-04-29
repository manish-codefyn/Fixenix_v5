from django.core.management.base import BaseCommand
from bookings.models import Device, DeviceBrand, DeviceModel

class Command(BaseCommand):
    help = 'Adds multiple device models to the database'

    def handle(self, *args, **kwargs):
        # Define the device types and their models
        device_models = {
         'Laptop': {
                 'Apple': [
                    # MacBook Series
                    'MacBook Pro 16-inch (M3)', 'MacBook Pro 14-inch (M3)',
                    'MacBook Pro 13-inch (M2)', 'MacBook Air 15-inch (M2)',
                    'MacBook Air 13-inch (M2)', 'MacBook Pro 16-inch (M2)',
                    'MacBook Pro 14-inch (M2)', 'MacBook Air 13-inch (M1)',
                    'MacBook Pro 16-inch (M1 Max)', 'MacBook Pro 14-inch (M1 Pro)',
                    'MacBook (12-inch)', 'MacBook Pro 15-inch (Intel)',
                    'MacBook Air (Intel)',
        ],

        'Dell': [
        'XPS 13 (2023)', 'XPS 15', 'Inspiron 15 5000', 'Latitude 7420', 'Alienware X17',
        'G5 15', 'Inspiron 14 5000', 'XPS 17', 'Latitude 5520', 'Precision 5750',
        'Vostro 15', 'Inspiron 7000', 'Dell G3 15', 
              ],
             'HP': [
        'Spectre x360 14', 'HP Envy 13', 'HP Pavilion 15', 'HP Elite Dragonfly', 'HP Omen 16',
        'HP EliteBook 850', 'HP Spectre x360 13', 'HP Pavilion x360', 'HP ProBook 450',
        'HP Chromebook 14', 'HP Omen 15', 'HP EliteBook 840', 'HP Envy x360',
            ],
           'Lenovo': [
        'ThinkPad X1 Carbon (9th Gen)', 'Legion 5 Pro', 'Yoga 9i', 'ThinkPad X1 Extreme Gen 4',
        'ThinkPad T14', 'Yoga 7i', 'Lenovo Ideapad 3', 'Legion 5i', 'ThinkPad L15',
        'Lenovo Flex 5', 'ThinkPad E15', 'IdeaPad Flex 5',
             ],
          'Asus': [
        'ZenBook 14 OLED', 'ROG Zephyrus G14', 'ROG Strix Scar 15', 'VivoBook 15', 'ROG Flow Z13',
        'Asus ExpertBook B1', 'Asus TUF Gaming F15', 'ZenBook Duo 14', 'Asus VivoBook Flip 14',
         'Asus ZenBook 13', 'ZenBook 14', 'Asus Chromebook Flip C434',
           ],
          'Acer': [
        'Predator Helios 300', 'Aspire 5', 'Acer Swift 3', 'Acer Chromebook Spin 713',
        'Acer Nitro 5', 'Aspire 7', 'Acer Swift 5', 'Acer Predator Triton 500',
        'Acer Aspire 1', 'Acer Spin 3', 'Acer Nitro 7',
           ],
         'MSI': [
        'GE76 Raider', 'GS66 Stealth', 'GF63 Thin', 'Creator Z16', 'Stealth GS75',
        'Alpha 15', 'Pulse GL66', 'GT76 Titan', 'MSI GE66 Raider', 'MSI Stealth GS65',
              ],
        'Samsung': [
        'Samsung Galaxy Book Pro 360', 'Samsung Notebook 9 Pro', 'Samsung Galaxy Book2', 
        'Samsung Galaxy Book', 'Samsung Chromebook Plus', 'Samsung Galaxy Book3 Ultra',
          ],
        'Microsoft': [
        'Surface Laptop 5', 'Surface Pro 9', 'Surface Laptop 4', 'Surface Book 3', 
        'Surface Laptop Go 2', 'Surface Pro 8', 'Surface Go 3', 'Surface Pro X',
            ],
        'Razer': [
        'Razer Blade 15 (2023)', 'Razer Blade Stealth 13', 'Razer Blade 17 (2023)', 'Razer Blade 14',
        'Razer Book 13', 'Razer Blade 15 Advanced', 
         ],
        'Alienware': [
        'Alienware X17', 'Alienware m15 R6', 'Alienware m17 R4', 'Alienware Aurora Ryzen',
        'Alienware Area-51m', 'Alienware m17', 'Alienware m15', 'Alienware X15',
         ],
         'Toshiba': [
        'Toshiba Portege X30', 'Toshiba Satellite Pro', 'Toshiba Tecra A50',
        'Toshiba Dynabook Satellite', 'Toshiba Satellite L55', 
         ],
         'LG': [
        'LG Gram 17', 'LG Gram 16', 'LG Gram 15', 'LG Gram 14', 'LG UltraGear',
        'LG Gram 14 2-in-1', 'LG Gram 15 2021', 'LG Gram 13', 
            ],
        'Huawei': [
        'Huawei MateBook X Pro', 'Huawei MateBook 13', 'Huawei MateBook D 15', 'Huawei MateBook 14', 
        'Huawei MateBook X', 'Huawei MateBook 16',
        ],
        'Sony': [
        'Sony VAIO SX14', 'VAIO Pro 13', 'VAIO Fit 15A', 'VAIO Z Flip',
        'VAIO S11', 'VAIO E Series', 
        ],
        'Fujitsu': [
        'Fujitsu Lifebook U9311', 'Fujitsu Stylistic Q7310', 'Fujitsu Lifebook E758', 
        'Fujitsu Lifebook A3510', 'Fujitsu Stylistic Q555',
         ],
        'Panasonic': [
        'Panasonic Toughbook 55', 'Panasonic Toughbook 33', 'Panasonic Toughbook 40', 
        'Panasonic CF-20', 'Panasonic CF-31', 
         ],
         'Chromebook': [
        'Google Pixelbook Go', 'Samsung Chromebook Plus', 'Acer Chromebook Spin 713', 
        'Lenovo Chromebook Duet', 'HP Chromebook x360', 
         ],
        'Google': [
        'Google Pixelbook', 'Google Pixelbook Go', 'Google Pixelbook 12.3', 
        'Google Chromebook Pixel', 
         ],
        'Gigabyte': [
        'Aorus 15G', 'Aorus 17G', 'Gigabyte Aero 15', 'Gigabyte Sabre 15', 'Gigabyte G5',
         ],
        'Xiaomi': [
        'Xiaomi Mi Notebook Pro 15', 'RedmiBook 15', 'Xiaomi Mi Notebook Air 13', 
        'RedmiBook 14', 'Xiaomi Mi Notebook Pro 14', 
         ],
        'VAIO': [
        'VAIO SX14', 'VAIO Z', 'VAIO S', 'VAIO SE', 'VAIO Pro 13', 'VAIO FE',
         ],
        'Clevo': [
        'Clevo P950HR', 'Clevo NH55AF', 'Clevo P775TM1-G', 
        'Clevo P870TM1', 'Clevo N950LF', 
         ],
        'Sager': [
        'Sager NP7858F2', 'Sager NP9155', 'Sager NP9658', 'Sager NP9570',
        'Sager NP9865', 
          ],
        'Eurocom': [
        'Eurocom Tornado F7', 'Eurocom Sky X9E3', 'Eurocom Q5',
        'Eurocom Panther 5', 
         ],
         'System76': [
        'System76 Oryx Pro', 'System76 Lemur Pro', 'System76 Galago Pro', 'System76 Thelio',
         ],
         'Origin PC': [
        'Origin EVO15-S', 'Origin NT-15', 'Origin PC Chronos', 'Origin EON17-X',
         ],
        'Notebook': [
        'Notebook Pro', 'Notebook Ultra', 'Notebook Flex', 
         ],
        'Chuwi': [
        'Chuwi HeroBook Pro', 'Chuwi UBook Pro', 'Chuwi LapBook Pro', 'Chuwi SurBook',
         ],
        'Infinix': [
        'Infinix Inbook X1', 'Infinix Inbook X2', 'Infinix Inbook X3',
         ],
        'Avita': [
        'Avita Liber V14', 'Avita Magus V14', 'Avita Pura', 'Avita Essential',
         ],
        'Dynabook': [
        'Dynabook Satellite Pro C50', 'Dynabook Tecra A50', 'Dynabook Portégé X30L',
         ],
         'Others': [
        'Generic Laptop Model 1', 'Custom Laptop Model 2', 
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
