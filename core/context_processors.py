from django.conf import settings


def notificacao_ms(request):
    context = {
        'NOTIFICACAO_MS_URL': settings.NOTIFICACAO_MS_URL,
        'NOTIFICACAO_MS_API_KEY': settings.NOTIFICACAO_MS_API_KEY,
    }

    if request.user.is_authenticated:
        context['NOTIFICACAO_USER_ID'] = request.user.id

    return context