from django.conf import settings


def site_settings(request):
    return {
    "SITE_NAME": settings.SITE_NAME,
    "NAVBAR_NAME": settings.NAVBAR_NAME,
    "SITE_EMAIL": settings.SITE_EMAIL,
    "NAV_ITEMS": settings.NAV_ITEMS,
    "CONTACT_NUMBER": settings.CONTACT_NUMBER,
    "EMAIL_ADDRESS": settings.EMAIL_ADDRESS,

}