from django.core.management.base import BaseCommand
from bookings.models import DeviceModel, DeviceProblem

class Command(BaseCommand):
    help = 'Adds multiple device problems to the database'

    def handle(self, *args, **kwargs):
        # Get all device models
        device_models = DeviceModel.objects.all()

        # Define common problems for each device model
        device_problems = {

         'iMac 24-inch (M3)': ['Screen discoloration', 'Bluetooth connectivity issues', 'System freezing'],
        'iMac Pro': ['Overheating under load', 'Display flickering', 'Fan noise issues'],
        'Mac Mini (M3)': ['USB port failure', 'Wi-Fi dropping frequently', 'Performance throttling'],
        'Mac Studio (M2 Ultra)': ['System not booting', 'Excessive fan noise', 'Bluetooth not working'],
        'Mac Pro (2023)': ['Overheating during heavy tasks', 'RAM compatibility issues', 'GPU driver crashes'],

        'Intel NUC 11 Performance': ['Overheating under load', 'Wi-Fi not working', 'Slow performance'],
        'Zotac MAGNUS One': ['GPU not detected', 'Fan noise', 'System freezing'],
        'ViewSonic VP2756-4K': ['Display flickering', 'Color accuracy issues', 'Screen not turning on'],
        'Thermaltake Core P5': ['Cooling issues', 'Overheating', 'Fan malfunction'],
              
       'System76 Thelio': ['Display issues', 'System freezing', 'Fan noise'],
        'System76 Galago Pro': ['Wi-Fi connectivity drops', 'Performance throttling', 'USB port failure'],
        # Add more Asus models here
           'Falcon Northwest Tiki': ['GPU overheating', 'Fan noise', 'System crashes'],
        'Falcon Northwest Talon': ['Slow performance', 'Wi-Fi not connecting', 'Overheating'],
        # Add more Acer models here
         'NZXT H510': ['Fan noise', 'Overheating', 'Performance throttling'],
        'NZXT Kraken G12': ['Cooling issues', 'System freezing', 'Display not working'],
    
        'Corsair Vengeance i7200': ['Overheating during gaming', 'Fan noise', 'RGB lighting issues'],
        'Corsair One Pro i200': ['GPU not detected', 'Wi-Fi connectivity issues', 'System freezing'],

        'Fujitsu Celsius R970': ['System not booting', 'GPU driver issues', 'Overheating'],
        'Fujitsu Workstation CELSIUS': ['Display not detected', 'Fan noise', 'Ethernet issues'],

        'IBM Netfinity': ['Ethernet not working', 'Power supply issues', 'System freezing'],
        'IBM eServer xSeries': ['Performance throttling', 'Overheating', 'Fan noise'],
        # Add more Samsung models here
        'Razer Tomahawk ATX': ['Overheating', 'GPU driver crashes', 'RGB lighting failure'],
        'Razer Blade Desktop': ['Wi-Fi signal issues', 'System freezing', 'Fan noise'],

         'Microsoft Surface Studio 2': ['Screen discoloration', 'Overheating', 'Wi-Fi connectivity issues'],
        'Microsoft Surface Hub 2S': ['Touchscreen unresponsive', 'Fan noise', 'System crashes'],

         'Samsung Odyssey Ark': ['Screen flickering', 'Bluetooth not working', 'Wi-Fi dropping'],
        'Samsung Smart Desktop': ['System freezing', 'Slow performance', 'Ethernet port issues'],


        'iMac 24-inch (M3)': ['Screen discoloration', 'Bluetooth connectivity issues', 'System freezing'],
        'iMac Pro': ['Overheating under load', 'Display flickering', 'Fan noise issues'],
        'Mac Mini (M3)': ['USB port failure', 'Wi-Fi dropping frequently', 'Performance throttling'],
        'Mac Studio (M2 Ultra)': ['System not booting', 'Excessive fan noise', 'Bluetooth not working'],
        'Mac Pro (2023)': ['Overheating during heavy tasks', 'RAM compatibility issues', 'GPU driver crashes'],
   
        'XPS Desktop': ['Overheating', 'USB-C port not working', 'Wi-Fi signal issues'],
        'Alienware Aurora R13': ['Fan making loud noise', 'System crashes during gaming', 'GPU overheating'],
        'Dell G5 Gaming Desktop': ['Slow performance under load', 'Power supply issues', 'Audio distortion'],
        'Dell OptiPlex 7090': ['Display output not working', 'Ethernet port failure', 'System not booting'],
 
        'HP Envy Desktop': ['Overheating', 'Fan noise', 'USB ports not working'],
        'HP Omen 30L': ['System crashing during games', 'GPU-related performance issues', 'RGB lighting not working'],
        'HP EliteDesk 800 G5': ['Ethernet not connecting', 'Overheating under load', 'RAM failure'],
        'HP Z8 G4 Workstation': ['Power supply overheating', 'CPU throttling', 'System freezing'],
    
        'Legion Tower 5': ['GPU overheating', 'Wi-Fi connectivity drops', 'System not booting'],
        'ThinkCentre M720q': ['Power supply issues', 'Display not detected', 'USB ports failing'],
        'ThinkStation P620': ['Fan noise during rendering tasks', 'Overheating under load', 'GPU driver crashes'],
        'Lenovo IdeaCentre AIO 3': ['Touchscreen unresponsive', 'Display flickering', 'System freezing'],
  
        'ROG Strix GA35': ['Overheating during gaming', 'Fan making noise', 'System not starting'],
        'Asus VivoPC': ['Wi-Fi not working', 'Bluetooth connectivity issues', 'Slow performance'],
        'Asus Chromebox 4': ['System crashes', 'Overheating', 'Keyboard and mouse lag'],
        'Asus Zen AiO': ['Display not turning on', 'Speakers not working', 'System freezing'],
   
  
        'Predator Orion 3000': ['System crashes during gaming', 'Fan noise', 'Overheating'],
        'Acer Aspire TC': ['Power supply issues', 'Slow performance', 'USB ports not working'],
        'Acer Nitro 50': ['GPU not detected', 'Display output failing', 'Wi-Fi connectivity issues'],
        'Acer Veriton X': ['System freezing', 'Overheating', 'Ethernet port not working'],
   
    
        'MSI Trident X': ['GPU driver issues', 'Overheating during gaming', 'Fan noise'],
        'MSI Creator P100X': ['Display not working', 'Wi-Fi not connecting', 'Performance throttling'],
        'MSI Infinite A': ['System not booting', 'USB ports failing', 'Ethernet issues'],
        'MSI Cubi 5': ['Overheating under load', 'Slow performance', 'Wi-Fi signal drops'],
    
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