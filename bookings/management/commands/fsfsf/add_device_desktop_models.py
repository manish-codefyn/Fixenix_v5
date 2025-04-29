from django.core.management.base import BaseCommand
from bookings.models import Device, DeviceBrand, DeviceModel

class Command(BaseCommand):
    help = 'Adds multiple device models to the database'

    def handle(self, *args, **kwargs):
        # Define the device types and their models
        device_models = {
    
    'Desktop': {
               'Apple': [
                    # iMac, Mac Mini, Mac Studio, Mac Pro
                    'iMac 24-inch (M3)', 'iMac 24-inch (M2)', 'iMac 27-inch (Intel)',
                    'iMac Pro', 'Mac Mini (M3)', 'Mac Mini (M2)', 'Mac Mini (M1)',
                    'Mac Studio (M2 Ultra)', 'Mac Studio (M1 Max)', 
                    'Mac Pro (2023)', 'Mac Pro (Intel)',
                ],
                  'Dell': [
        'XPS Desktop', 'Alienware Aurora R13', 'Dell Inspiron 3880', 'Dell Vostro 3670',
        'Dell OptiPlex 7090', 'Dell G5 Gaming Desktop', 'Dell XPS 8940', 'Dell Precision 5820',
    ],
    'HP': [
        'HP Envy Desktop', 'HP Pavilion Gaming Desktop', 'HP EliteOne 800 G6', 'HP ProDesk 400 G7',
        'HP Omen 30L', 'HP Z8 G4 Workstation', 'HP EliteDesk 800 G5', 'HP ProOne 600 G6',
    ],
    'Lenovo': [
        'Legion Tower 5', 'ThinkCentre M720q', 'IdeaCentre 5i', 'ThinkStation P620',
        'Legion Tower 7i', 'Lenovo ThinkCentre M90n', 'Lenovo ThinkStation P350', 'Lenovo IdeaCentre AIO 3',
    ],
    'Asus': [
        'ROG Strix GA35', 'Asus VivoPC', 'Asus ROG G20', 'Asus TUF Gaming Desktop', 'Asus ROG Strix GT15',
        'Asus Chromebox 4', 'Asus M32CD', 'Asus Zen AiO',
    ],
    'Acer': [
        'Predator Orion 3000', 'Acer Aspire TC', 'Acer Nitro 50', 'Acer Predator Orion 5000',
        'Acer Aspire C24', 'Acer Veriton X', 'Acer Revo Box', 'Acer ConceptD 100',
    ],
    'MSI': [
        'MSI Trident X', 'MSI Aegis RS', 'MSI MPG Infinite X', 'MSI Codex R', 
        'MSI MAG Infinite S3', 'MSI Creator P100X', 'MSI Infinite A', 'MSI Cubi 5',
    ],
    'Samsung': [
        'Samsung Odyssey Ark', 'Samsung Odyssey G5', 'Samsung Smart Desktop', 'Samsung S32A600',
    ],
    'Alienware': [
        'Alienware Aurora R13', 'Alienware Aurora R12', 'Alienware X17', 'Alienware Area-51m',
        'Alienware m15 R4', 'Alienware X51', 'Alienware Alpha',
    ],
    'Microsoft': [
        'Microsoft Surface Studio 2', 'Microsoft Surface Hub 2S', 'Microsoft Xbox Series X',
    ],
    'Razer': [
        'Razer Tomahawk ATX', 'Razer Core X', 'Razer Blade Desktop', 'Razer Blade 15 Advanced',
    ],
    'IBM': [
        'IBM Netfinity', 'IBM ThinkCentre A50', 'IBM eServer xSeries', 
    ],
    'Fujitsu': [
        'Fujitsu Celsius R970', 'Fujitsu Esprimo P556', 'Fujitsu Workstation CELSIUS',
    ],
    'Toshiba': [
        'Toshiba Dynabook Satellite', 'Toshiba Desktop Tecra', 'Toshiba Tecra A50',
    ],
    'Sony': [
        'Sony VAIO L Series', 'Sony VAIO C Series', 'Sony VAIO E Series', 
    ],
    'Panasonic': [
        'Panasonic Toughbook CF-31', 'Panasonic Toughbook CF-30', 'Panasonic Toughpad FZ-G1',
    ],
    'Intel NUC': [
        'Intel NUC 11 Performance', 'Intel NUC 10 Performance', 'Intel NUC 9 Extreme',
        'Intel NUC 8 Pro', 'Intel NUC 7',
    ],
    'Origin PC': [
        'Origin PC Chronos', 'Origin PC Neuron', 'Origin PC Millennium', 'Origin PC EON15-X',
    ],
    'CyberPowerPC': [
        'CyberPowerPC Gamer Xtreme', 'CyberPowerPC Gamer Supreme', 'CyberPowerPC Infinity X',
        'CyberPowerPC Zeus', 'CyberPowerPC Syber X',
    ],
    'iBUYPOWER': [
        'iBUYPOWER Gaming Desktop', 'iBUYPOWER Slate 4', 'iBUYPOWER Enthusiast', 'iBUYPOWER Revolt',
    ],
    'Corsair': [
        'Corsair Vengeance i7200', 'Corsair One Pro i200', 'Corsair Vengeance i1600', 'Corsair Vengeance i1400',
    ],
    'Gigabyte': [
        'AORUS Model X', 'Gigabyte AORUS 15G', 'Gigabyte BRIX', 'Gigabyte Aero 15', 
        'Gigabyte Z390 AORUS', 'Gigabyte AORUS 17G',
    ],
    'Thermaltake': [
        'Thermaltake Core P5', 'Thermaltake Level 20', 'Thermaltake View 71', 
    ],
    'NZXT': [
        'NZXT H510', 'NZXT H400', 'NZXT Kraken G12', 'NZXT S340', 
    ],
    'Maingear': [
        'Maingear Vybe', 'Maingear Rush', 'Maingear F131', 'Maingear Turbo', 
    ],
    'System76': [
        'System76 Thelio', 'System76 Oryx Pro', 'System76 Lemur Pro', 'System76 Galago Pro',
    ],
    'Zotac': [
        'Zotac MAGNUS One', 'Zotac ZBOX', 'Zotac ZBOX Sphere', 
    ],
    'Falcon Northwest': [
        'Falcon Northwest Tiki', 'Falcon Northwest Talon', 'Falcon Northwest FragBox', 
    ],
    'ViewSonic': [
        'ViewSonic VP2756-4K', 'ViewSonic XG2405', 'ViewSonic VX3276-2K', 
    ],
    'Eizo': [
        'Eizo ColorEdge CG319X', 'Eizo EV3285', 'Eizo FlexScan EV2750', 'Eizo Foris FS2735',
    ],
    'Others': [
        'Custom Desktop Model 1', 'Custom Desktop Model 2', 
    ],



            }}

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
