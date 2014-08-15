from django.contrib import admin
from bdt.volta.models import Userprofile
from bdt.volta.models import Ninguserprofile
from bdt.volta.models import Ninggroup
from bdt.volta.models import Ningevent
from bdt.volta.models import Skypeuserprofile
from bdt.volta.models import Skypegroup
from bdt.volta.models import Skypechatlog
from bdt.volta.models import Skypechatentry
from bdt.volta.models import Skypeurl
from bdt.volta.models import Skypememberlist
from bdt.volta.models import Googleuserprofile

admin.site.register(Userprofile)
admin.site.register(Ninguserprofile)
admin.site.register(Ninggroup)
admin.site.register(Ningevent)
admin.site.register(Skypeuserprofile)
admin.site.register(Skypegroup)
admin.site.register(Skypechatlog)
admin.site.register(Skypechatentry)
admin.site.register(Skypeurl)
admin.site.register(Skypememberlist)
admin.site.register(Googleuserprofile)
