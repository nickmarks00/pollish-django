from django.http import HttpResponse
from django.views import View
import logging

logger = logging.getLogger(__name__)

class PlaygroundView(View):

    def get(self, request, *args, **kwargs):
        logger.info('Hello from playground...')
        return HttpResponse('Hello, World!')