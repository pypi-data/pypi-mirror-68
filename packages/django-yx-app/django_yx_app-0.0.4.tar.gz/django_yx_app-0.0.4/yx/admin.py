from django.contrib import admin

from .models import YNote, YTag, YNotebook, YUser


class NoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(YNote, NoteAdmin)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(YTag, TagAdmin)


class YxAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(YUser, YxAccountAdmin)


class YNotebookAdmin(admin.ModelAdmin):
    pass


admin.site.register(YNotebook, YNotebookAdmin)
