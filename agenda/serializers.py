from rest_framework import serializers
from agenda.models import Agendamento
from django.utils import timezone
from datetime import timedelta, datetime

class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = ["id", "data_horario", "nome_cliente", "email_cliente", "telefone_cliente"]

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feita no passado")
        return value
    
    def validate_telefone_cliente(self, value):
        ac = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '(', ')', '+']
        if len(value) < 8:
            raise serializers.ValidationError("O número de telefone deve conter no mínimo 8 dígitos.")
        for i in value:
            if i not in ac:
                raise serializers.ValidationError("Telefone com formato inválido!")
            elif i == '+' and not value.startswith("+"):
                raise serializers.ValidationError("Para informar o código do país deve iniciar com +")
        return value
    
    def validate(self, attrs):
        data_horario = attrs.get("data_horario", "")
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        query = Agendamento.objects.filter(data_horario__day=data_horario.date().day, cancelado=False)
        delta = timedelta(minutes=30)        
        
        for i in query:            
            if data_horario.date().day == i.data_horario.day and email_cliente == i.email_cliente:
                raise serializers.ValidationError("Usuário já possui agendamento para o dia!")
            elif i.data_horario == data_horario:
                raise serializers.ValidationError("Horário já utilizado!")
            elif data_horario > (i.data_horario - delta) and data_horario < (i.data_horario + delta):
                raise serializers.ValidationError("É preciso de um intervalo de 30 minutos entre os agendamentos!")
            
        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
     
        return attrs
