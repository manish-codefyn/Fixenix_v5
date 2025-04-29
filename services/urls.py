from django.urls import path, include

from .views import (

    DoorstepServiceCreateView, 
    DoorstepServiceListView, 
    DoorstepServiceDetailView, 
    DoorstepServiceUpdateView,

    MobileAndTabServices,
    ComputerLaptopServices,
    CctvServices,
    DataRecoveryServices,
    ElectronicsServices,
    HardwareUpdateServices,
    IphoneRepairServicesView,
    SmartphoneRepairServicesView,
    LaptopRepairServicesView,
    DesktopRepairServicesView
)


urlpatterns = [
    path('best-desktop-repairing-siliguri/', DesktopRepairServicesView.as_view(), name='desktop-services'),
    path('best-laptop-repairing-siliguri/', LaptopRepairServicesView.as_view(), name='laptop-services'),
    path('best-mobile-repairing-siliguri/', SmartphoneRepairServicesView.as_view(), name='smartphone-services'),
    path('best-iphone-repair-services-siliguri/', IphoneRepairServicesView.as_view(), name='iphone-services'),
    path('best-doorstep-repairing-services-siliguri/', DoorstepServiceListView.as_view(), name='service-list'),
    path('best-doorstep-repairing-services-siliguri-book/', DoorstepServiceCreateView.as_view(), name='service-create'),
    path('best-doorstep-repairing-services-siliguri-book/<uuid:pk>/', DoorstepServiceDetailView.as_view(), name='service-detail'),
    path('best-doorstep-repairing-services-siliguri-book/<uuid:pk>/update/', DoorstepServiceUpdateView.as_view(), name='service-update'),
    path("best-laptop-desktop-repairing-services-siliguri-hardware-update/",HardwareUpdateServices.as_view(),name="hardware_update",),
    path("best-electronics-repairing-siliguri/", ElectronicsServices.as_view(), name="electronics_services",),
    path("best-data-recovery-services-siliguri/", DataRecoveryServices.as_view(),  name="data_recovery",),
    path("best-cctv-services-siliguri/",CctvServices.as_view(),  name="cctv_services",),
    path("best-mobile-repairing-siliguri/",MobileAndTabServices.as_view(),    name="mobile_tab_services", ),
    path("best-computer-laptop-repairing-services-siliguri/",ComputerLaptopServices.as_view(),    name="computer_laptop_services",),

]
