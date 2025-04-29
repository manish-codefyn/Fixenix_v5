from django.core.management.base import BaseCommand
from bookings.models import DeviceModel, DeviceProblem

class Command(BaseCommand):
    help = 'Adds multiple device problems to the database'

    def handle(self, *args, **kwargs):
        # Get all device models
        device_models = DeviceModel.objects.all()

        # Define common problems for each device model
        device_problems = {
            'Honor Pad 7': [
                'Touchscreen unresponsive in certain areas',
                'Battery drains faster than expected',
                'Wi-Fi connection keeps dropping',
                'Device freezes during updates',
                'No sound during video playback',
            ],
            'Honor Pad X6': [
                'Screen flickers during video playback',
                'Device overheating during gaming',
                'Charging port not working intermittently',
                'Slow performance during multitasking',
                'Unresponsive home button',
            ],
            'Chuwi HiPad X': [
                'Apps crash frequently',
                'Screen sensitivity issues',
                'Battery takes too long to charge',
                'Unstable Bluetooth connection',
                'Audio distortion during calls',
            ],
            'Chuwi Hi10 X': [
                'Touchscreen becomes unresponsive after software updates',
                'Tablet lags when using multiple apps',
                'Random shutdowns during video calls',
                'Device heats up during extended usage',
                'Wi-Fi connection drops after waking up from sleep mode',
            ],
            'Alldocube iPlay 40': [
                'Device lags when opening apps',
                'Battery drains too quickly on high-performance mode',
                'Apps fail to update properly',
                'Wi-Fi performance is inconsistent',
                'Device doesn\'t respond to touch sometimes',
            ],
            'Alldocube iPlay 30': [
                'Sound output becomes distorted after extended use',
                'Battery takes too long to charge',
                'Tablet freezes during high-graphic games',
                'Touchscreen lags after system update',
                'Bluetooth connection drops frequently',
            ],
            'Teclast T40 Plus': [
                'Device gets hot while using mobile data',
                'Apps freeze during usage',
                'Screen brightness issues in low light',
                'No notifications for incoming messages',
                'Touchscreen delay after updating firmware',
            ],
            'Teclast M40': [
                'Device freezes when switching between apps',
                'Charging port becomes loose over time',
                'Inconsistent GPS performance',
                'Battery not charging past 80%',
                'Touchscreen becomes unresponsive occasionally',
            ],
            'Teclast T10': [
                'Battery discharges even when device is off',
                'Apps crash on startup',
                'Wi-Fi connection drops frequently',
                'Device randomly restarts',
                'Charging time is longer than expected',
            ],
            'Panasonic Toughpad FZ-A2': [
                'Device screen becomes unresponsive after exposure to extreme temperatures',
                'Charging port is loose and requires adjustment',
                'Wi-Fi signal drops in certain areas',
                'Battery life significantly decreases over time',
                'Touchscreen slow to respond in certain modes',
            ],
            'Panasonic Toughbook A3': [
                'Device lags during app switching',
                'Battery takes too long to recharge',
                'Wi-Fi keeps disconnecting intermittently',
                'Sound cuts off intermittently during calls',
                'Camera app fails to launch sometimes',
            ],
            'Blackview Tab 8': [
                'Battery drains too quickly under heavy use',
                'Wi-Fi keeps disconnecting from networks',
                'App performance is slow',
                'Charging port stops working intermittently',
                'Touchscreen sensitivity issues in cold weather',
            ],
            'Blackview Tab 9': [
                'Device has screen flickering issues',
                'Unresponsive touchscreen at times',
                'Wi-Fi connectivity problems during video streaming',
                'Device overheating during gaming',
                'Battery does not last as long as advertised',
            ],
            'Microsoft Surface Pro 7': [
                'Wi-Fi disconnects when device is in sleep mode',
                'Battery life decreases significantly after updates',
                'Charging takes longer than expected',
                'Device occasionally freezes during heavy use',
                'Touchscreen becomes unresponsive intermittently',
            ],
            'Microsoft Surface Go': [
                'Screen turns black during video calls',
                'Wi-Fi connection drops randomly',
                'Charging port gets hot when plugged in',
                'Device becomes slow after recent updates',
                'Audio issues during media playback',
            ],
            'Microsoft Surface Book 3': [
                'Battery discharges rapidly',
                'Screen brightness not adjustable',
                'App performance lags during multitasking',
                'Wi-Fi signal drops intermittently',
                'Keyboard malfunctions under heavy use',
            ],
            'Archos 101b Oxygen': [
                'Device has performance issues with newer apps',
                'Screen freezes during multitasking',
                'Battery drains too quickly when in standby mode',
                'Device does not recognize external storage sometimes',
                'Charging port wears out too quickly',
            ],
            'Archos Core 101 3G': [
                'Screen flickers during video calls',
                'Wi-Fi connection unstable',
                'Battery charge indicator not accurate',
                'Apps do not install properly',
                'Device becomes slow after several apps installed',
            ],
            'ZTE Axon 7': [
                'Device experiences occasional crashes',
                'Audio distortion during video calls',
                'Touchscreen becomes unresponsive intermittently',
                'Battery fails to charge above 90%',
                'Wi-Fi connection drops constantly',
            ],
            'ZTE Blade Tab 8': [
                'Device freezes during video calls',
                'Camera fails to launch occasionally',
                'Charging port loose and unreliable',
                'Battery does not last as long as advertised',
                'Wi-Fi signal weak in certain areas',
            ],
            'Infinix Inbook X1': [
                'Device lags when switching between apps',
                'Wi-Fi connectivity issues',
                'Charging port malfunctions intermittently',
                'Device overheats during extended usage',
                'Touchscreen response delayed after updates',
            ],
            'Infinix Zero Tab': [
                'Screen brightness issues in low-light environments',
                'Battery does not charge properly',
                'Wi-Fi signal drops occasionally',
                'Apps crash when opened from recent apps',
                'Touchscreen becomes unresponsive at random times',
            ],
            'Motorola Moto Tab G20': [
                'Touchscreen lags when navigating apps',
                'Wi-Fi drops after sleep mode',
                'Apps fail to load properly',
                'Battery takes too long to charge',
                'Camera quality below expectations',
            ],
            'Motorola Moto Tab G70': [
                'Device overheating during gaming',
                'Charging port does not work intermittently',
                'Wi-Fi disconnects randomly',
                'Slow performance when using multiple apps',
                'Screen becomes unresponsive during media playback',
            ],
            'Nothing Phone': [
                'Device does not charge beyond 80%',
                'Battery drains faster than expected',
                'Apps crash randomly during usage',
                'Touchscreen response time is slow',
                'Wi-Fi connectivity issues',
            ],
                'Samsung Galaxy Tab S9 Ultra': [
            'Screen flickering', 'Battery draining quickly', 'Wi-Fi connectivity issues', 
            'App crashes', 'Touchscreen not responding'
        ],
        'Samsung Galaxy Tab S9+': [
            'Slow performance', 'Charging port malfunction', 'Bluetooth connection drops',
            'Overheating', 'Camera not working'
        ],
        'Samsung Galaxy Tab S9': [
            'Touchscreen sensitivity issues', 'Battery not charging', 'Laggy performance', 
            'Network signal issues', 'Display discoloration'
        ],
        'Samsung Galaxy Tab S8 Ultra': [
            'Audio distortion', 'Freezing during heavy apps usage', 'GPS not working', 
            'App compatibility issues', 'Cracked screen'
        ],
        'Samsung Galaxy Tab S8+': [
            'Battery not holding charge', 'Poor front camera quality', 'App freezing', 
            'Charging issues', 'Audio not working'
        ],
        'Samsung Galaxy Tab S8': [
            'Slow system performance', 'Low storage capacity', 'Display screen not responding',
            'Wi-Fi drops randomly', 'Touch gestures not working'
        ],
        'Samsung Galaxy Tab A8': [
            'Screen touch delay', 'App crashes', 'Battery overheating', 
            'Charging port issues', 'Random reboots'
        ],
        'Samsung Galaxy Tab Active3': [
            'Waterproof failure', 'Dustproof failure', 'Button malfunction', 
            'Performance lag', 'Wi-Fi not connecting'
        ],
        'Samsung Galaxy Tab S7 Ultra': [
            'App lag', 'Overheating during use', 'Charging issues', 
            'Cracked screen', 'Display malfunction'
        ],
        'Samsung Galaxy Tab S7+': [
            'Touchscreen unresponsiveness', 'Battery drains quickly', 'Wi-Fi signal weak', 
            'Slow charging', 'App freezes'
        ],
        'Samsung Galaxy Tab S7': [
            'Screen flickering', 'Touchscreen issues', 'App performance issues', 
            'Low battery life', 'Sound distortion'
        ],
        'Samsung Galaxy Tab A7': [
            'Battery does not charge', 'Device freezes', 'Touchscreen unresponsive', 
            'Overheating during charging', 'Weak Wi-Fi signal'
        ],
        'Samsung Galaxy Tab A7 Lite': [
            'App crashes', 'Screen unresponsiveness', 'Low storage space',
            'Battery drain', 'Device rebooting randomly'
        ],
        'Samsung Galaxy Tab E': [
            'No sound from speaker', 'Wi-Fi disconnects', 'Screen freezes', 
            'Charging issues', 'Camera malfunction'
        ],
        'Samsung Galaxy Tab 4': [
            'Touchscreen unresponsive', 'Slow processing', 'App crashing', 
            'Charging failure', 'No network connection'
        ],
        'Samsung Galaxy Tab 3': [
            'Display not turning on', 'Wi-Fi connectivity problems', 'Battery drains fast',
            'Audio issues', 'System crashes'
        ],
        'Samsung Galaxy View 2': [
            'Sound distortion', 'Screen flicker', 'Touchscreen issues', 
            'Slow response time', 'Overheating'
        ],
        'Samsung Galaxy TabPro S': [
            'Wi-Fi problems', 'Charging port issues', 'No audio', 
            'Overheating', 'App crash'
        ],
              'LG G Pad 5': [
                'Tablet lags when switching between apps',
                'Screen flickers intermittently',
                'Battery drains rapidly even in standby mode',
                'Wi-Fi connection unstable and drops randomly',
                'Sound distortion during video calls',
            ],
            'LG G Pad 8.0': [
                'Device overheating after extended use',
                'Touchscreen becomes unresponsive intermittently',
                'Bluetooth connection drops unexpectedly',
                'App crashes when loading heavy content',
                'Charging time is significantly longer than expected',
            ],

                     'TCL 10 TabMax': [
                'Screen brightness adjustment is slow',
                'Audio lags during video playback',
                'Tablet heats up during heavy use',
                'Wi-Fi connection drops intermittently',
                'Touchscreen is unresponsive after prolonged use',
            ],
            'TCL Tab 10s': [
                'Low battery life even with minimal usage',
                'Charging port is loose and disconnects easily',
                'Screen resolution is poor for high-definition videos',
                'App crashes frequently during use',
                'Tablet freezes during software updates',
            ],
            'Oppo Pad': [
                'Screen brightness not adjusting properly',
                'Touchscreen freezes intermittently during usage',
                'No audio from the speakers during video playback',
                'Wi-Fi signal strength weak in certain areas',
                'Battery drains faster than expected after recent update',
            ],
            'Oppo Pad Air': [
                'Charging port malfunctioning and causing intermittent charging',
                'Lagging when switching between apps or using heavy apps',
                'Bluetooth pairing issues with accessories',
                'Device becomes unresponsive after extended use',
                'Camera app freezes when trying to open or take a photo',
            ],
             'Vivo Pad': [
                'Screen touch sensitivity is inconsistent',
                'Tablet randomly restarts after prolonged use',
                'Low volume output even at maximum volume setting',
                'Wi-Fi disconnects frequently when idle',
                'Camera quality is poor with noticeable distortion',
            ],
             'Nokia T20': [
                'Screen touch sensitivity is inconsistent',
                'Tablet randomly restarts after prolonged use',
                'Low volume output even at maximum volume setting',
                'Wi-Fi disconnects frequently when idle',
                'Camera quality is poor with noticeable distortion',
            ],
            'Realme Pad': [
                'Screen flickering intermittently during video calls',
                'Battery drains too quickly while watching videos or playing games',
                'Device overheats during extended use',
                'Wi-Fi connectivity drops randomly',
                'Slow performance while multitasking or using heavy apps',
            ],
            'Realme Pad X': [
                'Bluetooth connectivity issues with headphones or speakers',
                'Touchscreen becomes unresponsive after prolonged usage',
                'Charging port is loose and causes inconsistent charging',
                'Slow charging despite using the original charger',
                'App crashes frequently after recent software update',
            ],
                'Lenovo Tab P11': [
                'Screen not turning on',
                'Battery charging issues',
                'Slow performance with multiple apps open',
                'Touchscreen unresponsive',
            ],
            'Lenovo Tab M10 Plus': [
                'WiFi disconnecting frequently',
                'Touchscreen glitches',
                'App crashes when multitasking',
                'Slow charging time',
            ],
            'Lenovo Yoga Tab 13': [
                'No sound from speakers',
                'Screen flickering during media playback',
                'Battery drains quickly during use',
                'WiFi issues while connected to hotspot',
            ],
            'Lenovo Tab M8': [
                'Performance lag while opening apps',
                'Charging port loose',
                'No notifications for apps',
                'Overheating during heavy usage',
            ],
            'Lenovo Tab K10': [
                'WiFi connectivity issues',
                'Screen freezes intermittently',
                'Slow response to touch input',
                'App loading delay',
            ],
            'Lenovo ThinkPad X1 Tablet': [
                'Battery not holding charge',
                'Screen brightness issues',
                'Keyboard not responsive',
                'USB-C port malfunctioning',
            ],
            # 
                        'Huawei MatePad Pro 12.6': [
                'Screen flickering on high brightness',
                'Battery charging issues',
                'WiFi connection drops frequently',
                'Touchscreen unresponsive',
            ],
            'Huawei MatePad 11': [
                'App crashes during multitasking',
                'Battery draining quickly during video playback',
                'Overheating during heavy use',
                'Slow charging with original charger',
            ],
            'Huawei MediaPad T5': [
                'Audio distortion when playing media',
                'Slow performance with multiple apps open',
                'Screen not responding to touch',
                'App crashes when opening camera',
            ],
            'Huawei MediaPad M5': [
                'Slow performance when switching apps',
                'WiFi connectivity issues',
                'Charging port not working properly',
                'Battery doesn’t last long on heavy use',
            ],
            'Huawei MediaPad T3': [
                'Touchscreen issues in cold weather',
                'Display brightness fluctuates',
                'Battery won’t charge past a certain percentage',
                'System slow after software updates',
            ],
            'Huawei MediaPad X2': [
                'Overheating when playing games',
                'WiFi signal weak even close to router',
                'Camera not focusing properly',
                'Screen freezing during video playback',
            ],
            # 
                      'Fire HD 10': [
                'Touchscreen unresponsive at times',
                'WiFi connection drops randomly',
                'Slow performance with multiple apps open',
                'Battery drains quickly during video playback',
            ],
            'Fire HD 8': [
                'Screen freezing during video playback',
                'Low volume during media playback',
                'Slow charging with original charger',
                'Apps crash during multitasking',
            ],
            'Fire 7': [
                'Lag when switching between apps',
                'Battery won’t charge above 60%',
                'Screen flickers under bright light',
                'Charging port not working properly',
            ],
            'Fire HD 10 Kids Edition': [
                'App crashes with parental controls enabled',
                'Overheating while playing games',
                'Slow performance on startup',
                'Audio issues during video calls',
            ],
            'Fire HD 8 Kids Edition': [
                'Touchscreen not responsive after screen lock',
                'Battery depletes faster than usual',
                'WiFi connectivity issues with apps',
                'Screen resolution issues in apps',
            ],
            # 
                       'Google Pixel Slate': [
                'Screen freezing intermittently',
                'Battery drains rapidly during use',
                'Wi-Fi connection drops frequently',
                'Keyboard connection issue via Bluetooth',
                'Slow performance with multiple apps open',
            ],
            'Google Pixel Tablet': [
                'Touchscreen becomes unresponsive after update',
                'Slow charging with official charger',
                'Screen flickering under bright light',
                'Lag when switching between apps',
                'Audio issues with certain apps',
            ],
            'Google Nexus 9': [
                'Battery not charging properly',
                'Performance lag in apps after system update',
                'Wi-Fi connectivity drops occasionally',
                'Display has color distortions on certain apps',
                'Touchscreen unresponsive in certain areas',
            ],
            # 
                      'Asus ZenPad 3S 10': [
                'Battery drains quickly during video playback',
                'Touchscreen becomes unresponsive intermittently',
                'Wi-Fi connectivity drops occasionally',
                'Performance lag in apps after system updates',
                'Bluetooth connectivity issues with accessories',
            ],
            'Asus Transformer Mini T102HA': [
                'Screen flickers when adjusting brightness',
                'Charging issues with certain cables',
                'Battery not charging properly',
                'Sluggish performance when using multiple apps',
                'Screen freezing when running intensive apps',
            ],
            'Asus VivoTab Smart': [
                'Wi-Fi signal strength is weak in certain areas',
                'Touchscreen not responding after waking from sleep',
                'Battery drains faster than expected',
                'Screen brightness issues in low light',
                'Slow app loading times',
            ],
                       'Acer Iconia Tab 10': [
                'Screen responsiveness issues when using apps',
                'Charging port malfunctioning or loose connection',
                'Wi-Fi signal drops after a few minutes of usage',
                'Battery drains quickly even on standby',
                'Bluetooth connectivity issues with headphones',
            ],
            'Acer Iconia One 8': [
                'Touchscreen lag while typing',
                'Device heats up quickly while charging',
                'Screen brightness flickers in low light',
                'Audio distortion when playing media through speakers',
                'Slow app performance after the latest update',
            ],
            'Acer Chromebook Tab 10': [
                'Apps crash frequently on startup',
                'Wi-Fi not connecting automatically after sleep mode',
                'Battery not charging beyond 80%',
                'Occasional screen freezes during multitasking',
                'Audio issues when using headphones',
            ],
                 'Dell Latitude 7320 Detachable': [
                'Screen flickers intermittently during high CPU usage',
                'Keyboard not responding after detaching from the tablet',
                'Battery drains quickly even with low usage',
                'Overheating issue during heavy tasks',
                'Wi-Fi connection drops when device goes to sleep',
            ],
            'Dell Venue 8 7000': [
                'Touchscreen is unresponsive at times',
                'Charging port is loose and not charging consistently',
                'Bluetooth disconnects when using wireless peripherals',
                'Low audio quality from speakers during media playback',
                'Frequent app crashes during multitasking',
            ],
                       'Sony Xperia Z4 Tablet': [
                'Screen freezes intermittently during video playback',
                'Battery drains faster than expected even with minimal use',
                'Touchscreen responsiveness issues during high brightness settings',
                'Wi-Fi connectivity drops after using for an extended period',
                'Slow performance when using multiple apps at the same time',
            ],
            'Sony Xperia Tablet Z': [
                'Charging port issues, not charging properly',
                'Overheating when playing graphics-intensive games',
                'Audio distortion when using speakers for media playback',
                'Bluetooth keeps disconnecting from paired devices',
                'Poor camera quality in low light conditions',
            ],
            'Sony Xperia Z3 Tablet Compact': [
                'Screen flickering when switching between apps',
                'Battery performance degrades quickly over time',
                'Touchscreen unresponsive during colder weather',
                'Wi-Fi connectivity issues, disconnecting frequently',
                'App crashes during multitasking or using resource-heavy apps',
            ],
                       'HP Elite x2 1012 G2': [
                'Touchscreen does not respond intermittently',
                'Keyboard disconnects unexpectedly from the device',
                'Battery drains faster even with low power usage',
                'Wi-Fi connectivity issues, disconnecting randomly',
                'Screen brightness adjusts automatically without user input',
            ],
            'HP Envy x2': [
                'Charging issues, device does not charge when plugged in',
                'Performance lags when running multiple apps simultaneously',
                'Audio distortion from speakers when playing videos',
                'Device heats up after extended usage, especially during gaming',
                'Bluetooth disconnects frequently from paired devices',
            ],
            'HP Spectre x2': [
                'Screen flickers when switching between apps or using certain software',
                'Battery drains abnormally quickly under heavy usage',
                'USB-C port stops working after a few months of use',
                'Wi-Fi signal weakens despite being near the router',
                'Touchpad fails to register clicks at times',
            ],
                       'Xiaomi Mi Pad 5': [
                'Screen unresponsiveness after the latest system update',
                'Battery drains too fast during gaming or media usage',
                'App crashes when using the camera',
                'Touchscreen exhibits ghost touches or sensitivity issues',
                'Audio output distorted during video playback',
            ],
            'Xiaomi Mi Pad 4': [
                'Device freezes on startup after the latest update',
                'Battery indicator shows incorrect charge percentage',
                'Bluetooth keeps disconnecting from paired devices',
                'Charging port becomes loose over time',
                'Performance lags while multitasking or using heavy apps',
            ],
            'Xiaomi Mi Pad 3': [
                'Device lags and stutters during gameplay or video streaming',
                'Wi-Fi drops intermittently or has weak signal strength',
                'Overheats during prolonged usage or gaming sessions',
                'Microphone fails to pick up sound clearly during video calls',
                'Touchscreen becomes unresponsive after a system update',
            ],
            'Surface Pro 9': [
                'Touchscreen not responding',
                'Battery draining rapidly',
                'Performance lag during multitasking',
                'Overheating during heavy use',
            ],
            'Surface Pro 8': [
                'WiFi disconnecting frequently',
                'Screen flickering during video playback',
                'Slow performance after system updates',
                'Charging port malfunctioning',
            ],
            'Surface Pro X': [
                'Keyboard not registering inputs',
                'Overheating during extended use',
                'Battery not charging',
                'Screen brightness flickers randomly',
            ],
            'Surface Go 3': [
                'Performance issues with apps',
                'Slow charging time',
                'No audio output through speakers',
                'WiFi connectivity issues',
            ],
            'Surface Go 2': [
                'Screen freezes intermittently',
                'Slow WiFi connection',
                'App crashes during heavy usage',
                'Touchscreen sensitivity problems',
            ],
            'Surface Duo 2': [
                'Battery drain issues',
                'Screen not turning on',
                'Performance lag while multitasking',
                'App crashing when switching screens',
            ],
            'Surface Duo': [
                'Touchscreen unresponsive',
                'WiFi signal drops',
                'App performance issues',
                'Camera not working correctly',
            ],

            'iPad Pro 12.9-inch (M2)': [
                   'Touchscreen unresponsive',
                    'Overheating while gaming',
                   'WiFi connectivity issues',
            ],
            'iPad Pro 11-inch (M2)': [
                'Battery draining quickly',
                'Camera lens distortion',
                'Performance lag when multitasking',
            ],
            'iPad Air (5th Generation)': [
                'Screen freezing during video calls',
                'Speakers not working properly',
                'Charging port malfunctioning',
            ],
            'iPad Air (4th Generation)': [
                'Battery not charging',
                'Display brightness flickering',
                'Bluetooth connection dropping',
            ],
            'iPad Mini (6th Generation)': [
                'Touch ID not functioning',
                'Overheating while watching videos',
                'Slow performance with multiple apps',
            ],
            'iPad Mini (5th Generation)': [
                'Screen distortion when watching movies',
                'Audio crackling during playback',
                'App crashing on startup',
            ],
            'iPad (10th Generation)': [
                'Screen cracking easily',
                'Charging issues',
                'Slow performance on heavy apps',
            ],
            'iPad (9th Generation)': [
                'Touchscreen ghosting',
                'Camera not focusing properly',
                'Sluggish performance after update',
            ],
            'iPad Pro 12.9-inch (M1)': [
                'Battery drain after update',
                'WiFi keeps disconnecting',
                'App performance issues',
            ],
            'iPad Pro 11-inch (M1)': [
                'Screen flickering intermittently',
                'Slow internet speed over WiFi',
                'Audio output distortion',
            ],
            'iPad Air (3rd Generation)': [
                'Display lag',
                'Poor WiFi reception',
                'Random reboots',
            ],
            'iPad Mini 4': [
                'Touchscreen not responding properly',
                'WiFi range is too short',
                'Performance lag while browsing',
            ],
            'iPad Pro 9.7-inch': [
                'Battery drains quickly',
                'Touchscreen issues',
                'Charging port loose',
            ],

  

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