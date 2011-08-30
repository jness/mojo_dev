
def template_shortcuts(request):
    from django.conf import settings
    cuts = {
        'url' : settings.BASE_URL,
        'js' : '%sjs/' % settings.STATIC_URL,
        'img' : '%simages/' % settings.STATIC_URL,
        'css' : '%scss/' % settings.STATIC_URL,
        }
    return cuts