from django.contrib import admin
from .models import UserRegistration, ListingModel,OwnerDetails,Booking,ProperFeedback,pymentdetails

admin.site.register(UserRegistration)
admin.site.register(pymentdetails)
admin.site.register(ListingModel)
admin.site.register([OwnerDetails,Booking])
admin.site.register(ProperFeedback)

admin.site.site_header = 'Administration Rental'                    # default: "Django Administration"
admin.site.index_title = 'Rental Admin APnel'                 # default: "Site administration"
admin.site.site_title = 'Adminsitration Panel'