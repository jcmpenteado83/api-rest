from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from agenda.models import Agendamento
from rest_framework.decorators import api_view
from agenda.serializers import AgendamentoSerializer
from rest_framework.response import Response

@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)
    if request.method == "GET":
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data)
    if request.method == "PATCH":
        serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "DELETE":
        obj.cancelado = True
        obj.save()
        return Response(status=204)


@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
    if request.method == "GET":
        query = Agendamento.objects.filter(cancelado=False)
        serializer = AgendamentoSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = request.data
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
