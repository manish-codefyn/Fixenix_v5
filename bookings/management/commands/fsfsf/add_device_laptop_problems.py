from django.core.management.base import BaseCommand
from bookings.models import DeviceModel, DeviceProblem

class Command(BaseCommand):
    help = 'Adds multiple device problems to the database'

    def handle(self, *args, **kwargs):
        # Get all device models
        device_models = DeviceModel.objects.all()

        # Define common problems for each device model
        device_problems = {

                    'MacBook Pro 16-inch (M3)': ['Battery drains quickly', 'Screen flickering', 'Wi-Fi connectivity issues'],
        'MacBook Pro 14-inch (M3)': ['Keyboard sticking', 'Performance throttling', 'Bluetooth connection drops'],
        # Add similar entries for other MacBook models
        'XPS 13 (2023)': ['Overheating', 'Battery not holding charge', 'Display flickering'],
        'XPS 15': ['Audio distortion', 'USB-C port not working', 'Trackpad lag'],
        'Inspiron 15 5000': ['Performance slowdown', 'Wi-Fi issues', 'Keyboard not responsive'],
        # Add more Dell models here

                    'Spectre x360 14': ['Overheating', 'Keyboard backlight not working', 'Fan noise'],
        'HP Envy 13': ['Wi-Fi signal issues', 'Touchpad not working', 'Screen ghosting'],
        'HP Pavilion 15': ['Slow system boot', 'Battery not charging fully', 'USB port malfunction'],
        # Add more HP models here
                    'ThinkPad X1 Carbon (9th Gen)': ['Battery swelling', 'Display flickering', 'System freezing'],
        'Legion 5 Pro': ['Performance throttling', 'Keyboard keys sticking', 'Fan issues'],
        'Yoga 9i': ['Screen discoloration', 'USB-C issues', 'Bluetooth connectivity issues'],
        # Add more Lenovo models here
        'ZenBook 14 OLED': ['Screen ghosting', 'Touchpad not responding', 'Wi-Fi dropping frequently'],
        'ROG Zephyrus G14': ['Overheating', 'Fan making noise', 'Keyboard unresponsive'],
        'Asus VivoBook 15': ['Battery not lasting long', 'Trackpad lagging', 'Bluetooth not connecting'],
        # Add more Asus models here
                    'Predator Helios 300': ['Fan issues', 'System crashes during gaming', 'Battery overheating'],
        'Aspire 5': ['Wi-Fi not connecting', 'Audio crackling', 'Display brightness issues'],
        'Acer Chromebook Spin 713': ['Keyboard malfunction', 'USB port issues', 'Touchscreen unresponsive'],
        # Add more Acer models here
          'GE76 Raider': ['GPU-related crashes', 'Battery drains quickly', 'System not booting'],
        'GS66 Stealth': ['Screen randomly going black', 'Touchpad freezing', 'Wi-Fi not working'],
        'GF63 Thin': ['Overheating', 'Performance throttling', 'Display issues'],
        # Add more MSI models here

    #         'Samsung Galaxy Book Pro 360': ['Display flickering', 'Keyboard backlight malfunction', 'Battery issues'],
        'Samsung Notebook 9 Pro': ['Wi-Fi connectivity issues', 'USB port failure', 'Fan noise'],
        'Samsung Galaxy Book': ['Performance lag', 'Screen discoloration', 'System freezing'],
        # Add more Samsung models here
        'MacBook Pro 16-inch (M3)': [
            'Overheating during prolonged use', 'Battery drains quickly', 
            'Screen flickering', 'Keyboard keys sticking', 'Wi-Fi connectivity issues'
        ],
        'MacBook Pro 14-inch (M3)': [
            'Audio distortion from speakers', 'Touchpad not responding', 
            'Performance throttling', 'Bluetooth connection drops', 'Display discoloration'
        ],
        'MacBook Pro 13-inch (M2)': [
            'Slow performance on heavy apps', 'Battery not charging fully', 
            'Screen ghosting', 'App freezing', 'Charging port malfunction'
        ],
        'MacBook Air 15-inch (M2)': [
            'Screen cracking easily', 'Fan noise issues', 'Trackpad lagging', 
            'System overheating', 'Battery swelling'
        ],
        'MacBook Air 13-inch (M2)': [
            'Wi-Fi signal weak', 'Keyboard backlight malfunction', 
            'System freezing randomly', 'Display flickering', 'No audio from speakers'
        ],
        'MacBook Pro 16-inch (M2)': [
            'GPU-related crashes', 'High fan noise', 'Battery draining while in sleep mode', 
            'USB-C port not working', 'Touch Bar issues'
        ],
        'MacBook Pro 14-inch (M2)': [
            'App compatibility issues', 'Slow system boot', 
            'MagSafe port not charging', 'Camera quality degradation', 'Touchpad unresponsive'
        ],
        'MacBook Air 13-inch (M1)': [
            'Overheating during multitasking', 'Bluetooth connection not stable', 
            'Display flicker at low brightness', 'Battery life not lasting as advertised', 'Speakers crackling'
        ],
        'MacBook Pro 16-inch (M1 Max)': [
            'Screen randomly going black', 'Fan speed issues', 'Touch Bar freezing', 
            'Wi-Fi not connecting', 'USB-C port failure'
        ],
        'MacBook Pro 14-inch (M1 Pro)': [
            'Battery swelling', 'Display hinge becoming loose', 'Keyboard not responsive', 
            'Audio popping sounds', 'Performance lag during video editing'
        ],
        'MacBook (12-inch)': [
            'Screen backlight malfunction', 'Performance slowdown', 
            'Battery life not lasting long', 'Wi-Fi randomly disconnecting', 'Touchpad sensitivity issues'
        ],
        'MacBook Pro 15-inch (Intel)': [
            'Excessive heating while charging', 'Keyboard double-typing', 
            'System freezing under heavy load', 'Fan noise is too loud', 'Battery expanding'
        ],
        'MacBook Air (Intel)': [
            'Low battery performance', 'Sluggish performance after updates', 
            'Overheating issues', 'Wi-Fi range reduced', 'No sound from speakers'
        ],
       'Surface Laptop 5': ['Touchscreen unresponsive', 'System overheating', 'Battery swelling'],
        'Surface Pro 9': ['Wi-Fi dropping frequently', 'Fan noise', 'Display brightness not adjusting'],
        'Surface Laptop Go 2': ['Performance lag', 'Keyboard unresponsive', 'Trackpad issues'],

        'Razer Blade 15 (2023)': ['Overheating during gaming', 'Fan making noise', 'Keyboard keys sticking'],
        'Razer Blade Stealth 13': ['Battery drains quickly', 'Wi-Fi not working', 'Display flickering'],
        'Razer Blade 17 (2023)': ['System crashing', 'USB-C port malfunction', 'Screen discoloration'],
       'LG Gram 17': ['Battery draining quickly', 'Performance throttling', 'Wi-Fi not connecting'],
        'LG Gram 16': ['Overheating', 'Display flickering', 'Fan noise issues'],
        'LG Gram 15': ['System not booting', 'Touchpad not working', 'Bluetooth connection issues'],
        'Toshiba Portege X30': ['Battery not charging', 'Fan noise issues', 'Touchpad lagging'],
        'Toshiba Satellite Pro': ['Screen discoloration', 'Wi-Fi signal weak', 'System freezing'],
        'Toshiba Tecra A50': ['Overheating', 'USB port malfunction', 'Keyboard backlight issues'],
        'MacBook Pro 16-inch (M3)': ['Battery drains quickly', 'Screen flickering', 'Wi-Fi connectivity issues'],
        'MacBook Pro 14-inch (M3)': ['Keyboard sticking', 'Performance throttling', 'Bluetooth connection drops'],
            # Add more models and problems as needed
        }

        problems = []
        for model_name, problem_list in device_problems.items():
            # Find the device model by name
            device_model = DeviceModel.objects.filter(name=model_name).first()
            
            if device_model:
                # Create problems for the device model
                for problem in problem_list:
                    problems.append(DeviceProblem(description=problem, device_model=device_model))

        # Bulk create the problems
        if problems:
            DeviceProblem.objects.bulk_create(problems)
            self.stdout.write(self.style.SUCCESS(f'{len(problems)} problems added successfully!'))
        else:
            self.stdout.write(self.style.WARNING('No problems were added because no matching device models were found!'))