from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from agenda.models import Agendamento
from rest_framework.decorators import api_view
from agenda.serializers import AgendamentoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics


class AgendamentoDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# class AgendamentoDetail(APIView):
#     def get(self, request, id):
#         obj = get_object_or_404(Agendamento, id=id)
#         serializer = AgendamentoSerializer(obj)
#         return JsonResponse(serializer.data)

#     def patch(self, request, id):
#         obj = get_object_or_404(Agendamento, id=id)
#         serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)
    
#     def delete(self, request, id):
#         obj = get_object_or_404(Agendamento, id=id)
#         obj.cancelado = True
#         obj.save()
#         return Response(status=200)

# @api_view(http_method_names=["GET", "PATCH", "DELETE"])
# def agendamento_detail(request, id):
#     obj = get_object_or_404(Agendamento, id=id)
#     if request.method == "GET":
#         serializer = AgendamentoSerializer(obj)
#         return JsonResponse(serializer.data)
#     if request.method == "PATCH":
#         serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)
#     if request.method == "DELETE":
#         obj.cancelado = True
#         obj.save()
#         return Response(status=204)


class AgendamentoList(
    mixins.ListModelMixin, # adicionar mixin de listagem
    mixins.CreateModelMixin, # adicionar mixin de criação
    generics.GenericAPIView, # classe genérica
):
    queryset = Agendamento.objects.filter(cancelado=False)
    serializer_class = AgendamentoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# class AgendamentoList(APIView):
#     def get(self, request):
#         query = Agendamento.objects.filter(cancelado=False)
#         serializer = AgendamentoSerializer(query, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     def post(self, request):
#         data = request.data
#         serializer = AgendamentoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
    

# @api_view(http_method_names=["GET", "POST"])
# def agendamento_list(request):
#     if request.method == "GET":
#         query = Agendamento.objects.filter(cancelado=False)
#         serializer = AgendamentoSerializer(query, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     if request.method == "POST":
#         data = request.data
#         serializer = AgendamentoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
