from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Advertisement
from .serializers import AdvertisementSerializer

from rest_framework.decorators import api_view


# Create your views here.


@api_view(['GET'])
def test(request, site, lookup_word):
    queryset = Advertisement.objects.filter(title__contains=lookup_word).filter(site=site)[:10]
    print(queryset)
    return Response(AdvertisementSerializer(queryset, many=True).data)