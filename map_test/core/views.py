from django.shortcuts import render
from django.views.generic import View
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import add_point, get_fusion_key
from .models import Address


class IndexView(View):

    def get(self, request):
        ctx = {
            'gkey': settings.GOOGLE_MAPS_KEY,
            'fusion_key': get_fusion_key(),
            'addresses': Address.objects.order_by('-id')
        }
        return render(request, 'index.html', context=ctx)


class AddressAditionView(APIView):
    """
    Endpoint for adding new addresses to the database

    expects:
    {
        "lat": string,
        "lon": string,
        "address": string
    }
    """
    def post(self, request):
        data = request.data
        address = add_point(data)
        return Response({'success': True, 'id': address.pk})
