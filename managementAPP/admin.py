from django.contrib import admin
from .models import Resident, Messege, Poll, Choice, Vote, newUser, InfoMessege

# Register your models here.
#admin.site.unregister(CustomUser)
#admin.site.unregister(Resident)
admin.site.register(newUser)

admin.site.register(Messege)
admin.site.register(InfoMessege)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)