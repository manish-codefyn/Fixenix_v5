from django.core.management.base import BaseCommand
from bookings.models import Device, DeviceBrand, DeviceModel

class Command(BaseCommand):
    help = 'Adds multiple device models to the database'

    def handle(self, *args, **kwargs):
        # Define the device types and their models
        device_models = {

        'Mobile': {
                    'Apple': [
                    # iPhone Series
                    'iPhone 15 Pro Max', 'iPhone 15 Pro', 'iPhone 15', 'iPhone 15 Plus',
                    'iPhone 14 Pro Max', 'iPhone 14 Pro', 'iPhone 14', 'iPhone 14 Plus',
                    'iPhone 13 Pro Max', 'iPhone 13 Pro', 'iPhone 13', 'iPhone 13 Mini',
                    'iPhone 12 Pro Max', 'iPhone 12 Pro', 'iPhone 12', 'iPhone 12 Mini',
                    'iPhone SE (3rd Generation)', 'iPhone SE (2nd Generation)',
                    'iPhone 11 Pro Max', 'iPhone 11 Pro', 'iPhone 11',
                    'iPhone XS Max', 'iPhone XS', 'iPhone XR', 'iPhone X',
                    'iPhone 8 Plus', 'iPhone 8', 'iPhone 7 Plus', 'iPhone 7',
                    'iPhone 6S Plus', 'iPhone 6S',
                ],

                'Samsung': [
                    # Galaxy S Series
                    'Galaxy S23', 'Galaxy S23+', 'Galaxy S23 Ultra',
                    'Galaxy S22', 'Galaxy S22+', 'Galaxy S22 Ultra',
                    'Galaxy S21', 'Galaxy S21+', 'Galaxy S21 Ultra',
                    'Galaxy S20', 'Galaxy S20+', 'Galaxy S20 Ultra',
                    'Galaxy S10', 'Galaxy S10+', 'Galaxy S10e',
                    
                    # Galaxy Note Series
                    'Galaxy Note 20', 'Galaxy Note 20 Ultra',
                    'Galaxy Note 10', 'Galaxy Note 10+', 'Galaxy Note 10 Lite',
                    'Galaxy Note 9', 'Galaxy Note 8',
                    
                    # Galaxy Z Series (Foldable)
                    'Galaxy Z Fold 5', 'Galaxy Z Fold 4', 'Galaxy Z Fold 3', 'Galaxy Z Fold 2',
                    'Galaxy Z Flip 5', 'Galaxy Z Flip 4', 'Galaxy Z Flip 3', 'Galaxy Z Flip',
                    
                    # Galaxy A Series (Mid-range)
                    'Galaxy A73', 'Galaxy A72', 'Galaxy A71', 'Galaxy A70',
                    'Galaxy A53', 'Galaxy A52', 'Galaxy A51', 'Galaxy A50',
                    'Galaxy A33', 'Galaxy A32', 'Galaxy A31', 'Galaxy A30',
                    
                    # Galaxy M Series (Budget and Mid-range)
                    'Galaxy M54', 'Galaxy M53', 'Galaxy M52', 'Galaxy M51',
                    'Galaxy M32', 'Galaxy M31', 'Galaxy M22', 'Galaxy M21',
                    
                    # Galaxy F Series (Budget-focused)
                    'Galaxy F62', 'Galaxy F41', 'Galaxy F12',
                    
                    # Other Series
                    'Galaxy J7', 'Galaxy J5', 'Galaxy J3', 
                    'Galaxy XCover Pro', 'Galaxy XCover 5',
                    
                    # Tablets (Optional for Comprehensive Coverage)
                    'Galaxy Tab S9', 'Galaxy Tab S8', 'Galaxy Tab S7',
                    'Galaxy Tab A8', 'Galaxy Tab A7', 'Galaxy Tab Active 3',
                    
                    # Older Devices
                    'Galaxy S8', 'Galaxy S9', 'Galaxy S10 Lite',
                    'Galaxy Note Edge', 'Galaxy Note 4'
                ],
            
               'OnePlus': [
               'OnePlus 11', 'OnePlus 10 Pro', 'OnePlus 9R', 'OnePlus 8T', 'OnePlus Nord 2T', 
                'OnePlus 7 Pro', 'OnePlus 5T', 'OnePlus Nord CE 3 Lite', 'OnePlus 8 Pro', 
               'OnePlus 6T', 'OnePlus 6', 'OnePlus 7T', 'OnePlus 9 Pro', 'OnePlus X', 
                ],
               'Xiaomi': [
        'Mi 13 Ultra', 'Mi 12', 'Redmi Note 12 Pro', 'Redmi Note 11T', 'Poco X5 Pro', 
        'Mi Mix 4', 'Redmi K40 Gaming', 'Mi A3', 'Redmi Note 9', 'Redmi Note 8 Pro',
        'Mi 11X', 'Mi 10', 'Redmi 9', 'Redmi 10 Prime', 'Mi 9T Pro', 'Redmi K30',
    ],
    'Redmi': [
        'Redmi Note 12', 'Redmi 11 Prime', 'Redmi 10 Power', 'Redmi 9 Activ',
        'Redmi K50 Pro', 'Redmi 8A Dual', 'Redmi 10A', 'Redmi Note 11', 'Redmi K20',
        'Redmi Note 10', 'Redmi Note 9 Pro', 'Redmi Note 8', 'Redmi Note 7',
        'Redmi 9A', 'Redmi 9C', 'Redmi Note 9 Pro Max', 'Redmi 10', 'Redmi Note 10 Pro',
        'Redmi K30 Pro', 'Redmi K40', 'Redmi 8', 'Redmi 7', 'Redmi S2'
    ],
    'Realme': [
        'Realme GT Neo 5', 'Realme 11 Pro+', 'Realme C55', 'Realme Narzo 60X',
        'Realme X7 Max', 'Realme 9i', 'Realme 8 Pro', 'Realme GT 2 Pro', 'Realme 7 Pro',
        'Realme 11 5G', 'Realme Narzo 50A', 'Realme X50 Pro', 'Realme Narzo 30 Pro',
        'Realme 8 5G', 'Realme C11', 'Realme Narzo 30A', 'Realme GT Master Edition', 
        'Realme 6 Pro', 'Realme 6', 'Realme 7 5G'
    ],
    'Oppo': [
        'Oppo Find X6 Pro', 'Oppo Reno 10', 'Oppo F23 5G', 'Oppo A78', 
        'Oppo A17', 'Oppo K10', 'Oppo A54', 'Oppo F19 Pro', 'Oppo F19',
        'Oppo A15s', 'Oppo Reno 5 Pro 5G', 'Oppo Reno 4', 'Oppo F9',
        'Oppo Reno 6 Pro 5G', 'Oppo A74 5G', 'Oppo F19s', 'Oppo A95', 'Oppo A53', 
        'Oppo F17 Pro', 'Oppo A31', 'Oppo Reno 2F', 'Oppo Reno 2', 'Oppo A12', 
        'Oppo A11k', 'Oppo F5', 'Oppo A83', 'Oppo F3', 'Oppo R17 Pro', 'Oppo F1s', 
        'Oppo A37', 'Oppo F1', 'Oppo A5 2020', 'Oppo A9 2020', 'Oppo R15 Pro'
    ],
    'Vivo': [
           'Vivo X90 Pro', 'Vivo Y100', 'Vivo V27e', 'Vivo T2x', 'Vivo Y20G', 
         'Vivo Z1 Pro', 'Vivo X60 Pro', 'Vivo V15 Pro', 'Vivo V21e', 
    'Vivo Y30', 'Vivo Y91i', 'Vivo Y11', 'Vivo V17 Pro',
    'Vivo V23 Pro', 'Vivo X70 Pro', 'Vivo V20', 'Vivo V19', 'Vivo Y53s', 
    'Vivo V17', 'Vivo Y15', 'Vivo Y12s', 'Vivo Y20', 'Vivo Z5x', 'Vivo Y21', 
    'Vivo Z3i', 'Vivo X9s', 'Vivo X21', 'Vivo U10', 'Vivo V3 Max', 'Vivo Y95',
    'Vivo S1 Pro', 'Vivo Y55s', 'Vivo V5 Plus', 'Vivo S1', 'Vivo Y91', 'Vivo Y91C'
    ],
    'Huawei': [
        'Huawei Mate 60 Pro', 'Huawei P60 Art', 'Huawei Nova 11', 'Huawei Y9 Prime', 
        'Huawei Honor 9X', 'Huawei Mate 50', 'Huawei P40 Pro', 'Huawei Mate 40 Pro',
        'Huawei P30 Pro', 'Huawei Nova 5T', 'Huawei Honor 20', 'Huawei Honor 10',
    ],
    'Google': [
        'Pixel 8', 'Pixel 7 Pro', 'Pixel 6a', 'Pixel 5', 'Pixel 4a 5G', 
        'Pixel 3 XL', 'Pixel 2', 'Pixel 2 XL', 'Pixel 3a', 'Pixel 6', 
        'Pixel 4', 'Pixel 4 XL', 'Pixel 7', 
    ],
    'Motorola': [
           'Moto Edge 40', 'Moto G73', 'Moto Razr+ (2023)', 'Moto G32', 
    'Moto E13', 'Moto G9 Power', 'Moto E7 Plus', 'Moto G50', 'Moto G6',
    'Moto Z3', 'Moto X4', 'Moto E4 Plus', 'Moto Z2 Force',
    'Moto Edge 30', 'Moto G62', 'Moto G82', 'Moto G60', 'Moto G71', 
    'Moto One Fusion+', 'Moto One Vision', 'Moto Z4', 'Moto G6 Play', 
    'Moto Z2 Play', 'Moto G5 Plus', 'Moto X Style', 'Moto X Play', 
    'Moto E6 Plus', 'Moto G5S', 'Moto G4 Plus', 'Moto E6', 'Moto Z Force'
    ],
    'Nokia': [
    'Nokia XR21', 'Nokia G42', 'Nokia C12 Pro', 'Nokia G60', 
    'Nokia 5310 (2020)', 'Nokia 8.3', 'Nokia 7.2', 'Nokia 6.2', 'Nokia 5.3',
    'Nokia 2.4', 'Nokia 1.4', 'Nokia 3.4', 
    'Nokia X100', 'Nokia X10', 'Nokia 9 PureView', 'Nokia 6.1 Plus', 
    'Nokia 5.4', 'Nokia 8.1', 'Nokia 7.1', 'Nokia 2.3', 'Nokia 1.3', 
    'Nokia 3.1 Plus', 'Nokia 4.2', 'Nokia 3.1', 'Nokia 2.1', 'Nokia 6.1',
    'Nokia 9.1 PureView', 'Nokia C30', 'Nokia 2.2', 'Nokia 3.2', 'Nokia 5.1 Plus'
    ],
    'Sony': [
        'Sony Xperia 1 V', 'Sony Xperia 10 IV', 'Sony Xperia 5 III', 'Sony Xperia Pro-I', 
        'Sony Xperia XA2', 'Sony Xperia XZ3', 'Sony Xperia XZ2 Premium', 'Sony Xperia XZ1',
        'Sony Xperia 10 Plus', 'Sony Xperia XZ', 'Sony Xperia L4', 'Sony Xperia 5 II',
    ],
    'Asus': [
        'Asus ROG Phone 7', 'Asus Zenfone 10', 'Asus ROG Phone 6', 'Asus Zenfone 9', 
        'Asus ROG Phone 5', 'Asus Zenfone 8', 'Asus Zenfone 7 Pro', 'Asus ROG Phone 4',
        'Asus Zenfone 6', 'Asus Zenfone 5Z', 
    ],
    'LG': [
        'LG Wing', 'LG Velvet', 'LG G8X ThinQ', 'LG K42', 'LG V60 ThinQ', 
        'LG G7 ThinQ', 'LG Q7', 'LG V50', 'LG G6', 'LG Stylo 6', 'LG G8',
    ],
   'Micromax': [
    'Micromax IN 2b', 'Micromax IN Note 2', 'Micromax Bharat 2 Plus', 
    'Micromax Canvas Infinity', 'Micromax IN 1', 'Micromax IN Note 1',
    'Micromax IN 2c', 'Micromax IN Note 3', 'Micromax Bharat 4', 'Micromax A104',
    'Micromax Canvas 2', 'Micromax Canvas 5', 'Micromax Q412', 'Micromax Bharat 5 Plus',
],

'Infinix': [
    'Infinix Zero Ultra', 'Infinix Zero 5G', 'Infinix Note 12 Pro', 'Infinix Smart 6', 
    'Infinix Hot 12', 'Infinix Note 10', 'Infinix Zero 30', 'Infinix Note 8',
    'Infinix Zero 8i', 'Infinix Note 11 Pro', 'Infinix Hot 11', 'Infinix Note 7', 
    'Infinix S5 Pro', 'Infinix Zero 6', 'Infinix Hot 10S', 
],

'Tecno': [
    'Tecno Phantom V Fold', 'Tecno Spark 10 Pro', 'Tecno Pova 5G', 
    'Tecno Camon 19 Pro', 'Tecno Pova Neo', 'Tecno Camon 20', 'Tecno Spark 9T',
    'Tecno Spark 9', 'Tecno Pova 3', 'Tecno Phantom X', 'Tecno Camon 18T',
    'Tecno Pova 2', 'Tecno Camon 16', 'Tecno Spark 7', 
],

'Lava': [
    'Lava Blaze 5G', 'Lava Z3', 'Lava Agni 2 5G', 'Lava X2', 
    'Lava Z6', 'Lava Iris X1', 'Lava A5', 
    'Lava Z4', 'Lava Agni 1', 'Lava Z2', 'Lava Blaze NXT', 
    'Lava X10', 'Lava Iris 450', 'Lava KKT 40', 
],

'iQOO': [
    'iQOO Neo 7 Pro', 'iQOO Z7', 'iQOO 11', 'iQOO 9T', 'iQOO Z6',
    'iQOO 7 Legend', 'iQOO Z5', 'iQOO Neo 5', 
    'iQOO Z8', 'iQOO 9', 'iQOO Neo 6', 'iQOO Z6 5G',
    'iQOO 8 Pro', 'iQOO 7', 'iQOO Z7 5G',
],

'ZTE': [
    'ZTE Axon 50 Ultra', 'ZTE Blade V40 Vita', 'ZTE Nubia Z50S Pro', 
    'ZTE Axon 30', 'ZTE Blade V9', 'ZTE Axon 20', 
    'ZTE Blade V30', 'ZTE Axon 10 Pro', 'ZTE Blade A7', 
    'ZTE Nubia RedMagic 8 Pro', 'ZTE Axon 9 Pro', 'ZTE Blade A5',
],
    'Honor': [
        'Honor Magic V2', 'Honor 90 Pro', 'Honor X9a', 'Honor Play 7T', 
        'Honor 50', 'Honor X8', 'Honor 8X', 'Honor 30 Pro',
    ],
    'Meizu': [
        'Meizu 20 Infinity', 'Meizu 18 Pro', 'Meizu 17', 'Meizu 16s Pro', 
        'Meizu Note 9', 'Meizu 15 Plus', 
    ],
    'BlackBerry': [
        'BlackBerry Key2', 'BlackBerry Evolve', 'BlackBerry Passport', 
        'BlackBerry Z10', 'BlackBerry Bold 9900', 
    ],
    'HTC': [
        'HTC Desire 22 Pro', 'HTC Wildfire X', 'HTC U20 5G', 
        'HTC One M8', 'HTC One M7', 
    ],
    'Lenovo': [
        'Lenovo Legion Y70', 'Lenovo K14 Plus', 'Lenovo Z6 Pro', 'Lenovo Z5', 
        'Lenovo K10 Note', 'Lenovo A7000', 'Lenovo S5', 
    ],
    'Poco': [
        'Poco F5', 'Poco X5 Pro', 'Poco M5', 'Poco C55', 
        'Poco F4', 'Poco X4 Pro 5G', 'Poco M2 Pro',
    ],
    'Nothing': [
        'Nothing Phone (2)', 'Nothing Phone (1)', 
    ],
    'Fairphone': [
        'Fairphone 5', 'Fairphone 4', 'Fairphone 3+', 
    ],
    'TCL': [
        'TCL 40 X', 'TCL 30 V 5G', 'TCL 20 Pro 5G', 'TCL 10 Pro',
        'TCL 10L', 
    ],
    'Alcatel': [
        'Alcatel 3L', 'Alcatel 1B', 'Alcatel 1X', 'Alcatel Idol 4S', 
        'Alcatel 3V', 'Alcatel 5V',
    ],
    'Gionee': [
        'Gionee Max', 'Gionee F8 Neo', 'Gionee K10', 'Gionee M11',
    ],
    'Coolpad': [
        'Coolpad Cool 20 Pro', 'Coolpad Legacy', 'Coolpad Mega 5A', 'Coolpad Note 3',
    ],
    'Others': [
        'Generic Model 1', 'Generic Model 2', 'Custom Model', 
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
