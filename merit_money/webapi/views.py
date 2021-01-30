from django.shortcuts import render
import datetime
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework import generics
import datetime
import uuid
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User
from .models import Cargo, Setor, Premios, Transacao, TransacaoPremios, Colaborador
from .serializers import CargoSerializer, SetorSerializer, PremiosSerializer, TransacaoSerializer, TransacaoPremiosSerializer, ColaboradorSerializer
from django.views.decorators.csrf import csrf_exempt  # Create your views here.


@authentication_classes([])
@permission_classes([])
class CargoViewSet(viewsets.ModelViewSet):

    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


@authentication_classes([])
@permission_classes([])
class SetorViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    queryset = Setor.objects.all()
    serializer_class = SetorSerializer

@authentication_classes([])
@permission_classes([])
class PremiosViewSet(viewsets.ModelViewSet):

    queryset = Premios.objects.all()
    serializer_class = PremiosSerializer


@api_view(['POST'])
def resgatar_premio(request):
    showtime = datetime.datetime.now().strftime("%Y-%m-%d")
    colaborador = Colaborador.objects.get(pk=request.data['id_colaborador'])
    premio = Premios.objects.get(pk=request.data['id_premio'])

    if colaborador.saldo_recebido >= premio.valor:
        colaborador.saldo_recebido -= premio.valor
        colaborador.premios.add(premio)
        colaborador.save()
        transacao = TransacaoPremios(
            str(uuid.uuid1().hex), showtime, request.data['id_premio'], request.data['id_colaborador'])
        transacao.save()

        return Response(status=status.HTTP_200_OK)
    else:
        return Response({"error": "O remetente não tem moedas o suficiente"}, status=status.HTTP_400_BAD_REQUEST)


class TransacaViewSet(viewsets.ModelViewSet):
    serializer_class = TransacaoSerializer
    queryset = Transacao.objects.all()

    def get_queryset(self):
        queryset = Transacao.objects.all()
        data = self.request.query_params.get('data', None)
        remetente = self.request.query_params.get('remetente', None)
        destinatario = self.request.query_params.get('destinatario', None)

        params = {}

        if(data is not None):
            params['data_transacao'] = data
        if(remetente is not None):
            params['id_remetente'] = remetente
        if(destinatario is not None):
            params['id_destinatario'] = destinatario

        queryset = queryset.filter(**params)

        return queryset

@authentication_classes([])
@permission_classes([])
class TransacaoPremiosViewSet(viewsets.ModelViewSet):
    serializer_class = TransacaoPremiosSerializer
    queryset = TransacaoPremios.objects.all()

    def get_queryset(self):
        queryset = TransacaoPremios.objects.all()
        start_date = self.request.query_params.get('start-date', None)
        end_date = self.request.query_params.get('end-date', None)
        premio_resgatado = self.request.query_params.get(
            'premio-resgatado', None)
        id_colaborador = self.request.query_params.get('colaborador', None)

        params = {}

        if(start_date is not None):
            params['data_transacao__gte'] = start_date
        if(end_date is not None):
            params['data_transacao__lte'] = end_date
        if(premio_resgatado is not None):
            params['premio_resgatado'] = premio_resgatado
        if(id_colaborador is not None):
            params['id_colaborador'] = id_colaborador

        queryset = queryset.filter(**params)

        return queryset


@authentication_classes([])
@permission_classes([])
class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer


@api_view(['POST'])
def send_coins(request):
    showtime = datetime.datetime.now().strftime("%Y-%m-%d")

    remetente = Colaborador.objects.get(pk=request.data['id_remetente'])
    destinatario = Colaborador.objects.get(pk=request.data['id_destinatario'])

    if remetente is not destinatario:
        if remetente.saldo_acumulado >= request.data['valor']:
            remetente.saldo_acumulado -= request.data['valor']
            destinatario.saldo_recebido += request.data['valor']
        else:
            return Response({"error": "O remetente não tem moedas o suficiente"}, status=status.HTTP_204_NO_CONTENT)

        transacao = Transacao(str(uuid.uuid1(
        ).hex), showtime, request.data['id_remetente'], request.data['id_destinatario'], request.data['valor'], request.data['justificativa'])

        remetente.save()
        destinatario.save()
        transacao.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def lista_doacoes_colaborador(request, id_colaborador):
    doacoes_realizadas = Transacao.objects.filter(
        id_remetente=id_colaborador).order_by('-data_transacao')
    doacoes_recebidas = Transacao.objects.filter(
        id_destinatario=id_colaborador).order_by('-data_transacao')

    serializer_realizadas = TransacaoSerializer(doacoes_realizadas, many=True)
    serializer_recebidas = TransacaoSerializer(doacoes_recebidas, many=True)

    for remetente in serializer_realizadas.data:
        if(remetente['id_remetente']):
            remetente['nome_remetente'] = ColaboradorSerializer(Colaborador.objects.get(
                id=remetente['id_remetente'])).data['nome']
    for destinatario in serializer_realizadas.data:
        if(destinatario['id_destinatario']):
            destinatario['nome_destinatario'] = ColaboradorSerializer(Colaborador.objects.get(
                id=destinatario['id_destinatario'])).data['nome']
    for remetente in serializer_recebidas.data:
        if(remetente['id_remetente']):
            remetente['nome_remetente'] = ColaboradorSerializer(Colaborador.objects.get(
                id=remetente['id_remetente'])).data['nome']
    for destinatario in serializer_recebidas.data:
        if(destinatario['id_destinatario']):
            destinatario['nome_destinatario'] = ColaboradorSerializer(Colaborador.objects.get(
                id=destinatario['id_destinatario'])).data['nome']

    response_api = {"realizadas": serializer_realizadas.data,
                    "recebidas": serializer_recebidas.data}

    return Response(response_api, status=status.HTTP_200_OK)


@ api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    colaborador = Colaborador.objects.filter(user_id=serializer.data['id'])
    colaborador_serializer = ColaboradorSerializer(colaborador, many=True)
    return Response({"user": serializer.data, "colaborador": colaborador_serializer.data[0]})


@ authentication_classes([])
@ permission_classes([])
class UserList(APIView):

    def post(self, request, format=None):
        user_serializer = UserSerializerWithToken(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            colaborador = Colaborador()
            colaborador.user = user
            colaborador.nome = request.data['nome']
            colaborador.sobrenome = request.data['sobrenome']
            colaborador.cargo = Cargo.objects.get(pk=request.data['cargo'])
            colaborador.setor = Setor.objects.get(pk=request.data['setor'])
            colaborador.saldo_acumulado = 20
            colaborador.saldo_recebido = 0
            colaborador.save()

            get_colaborador = Colaborador.objects.filter(
                nome=request.data['nome'], sobrenome=request.data['sobrenome'])
            get_colaborador_serializer = ColaboradorSerializer(
                get_colaborador, many=True)

            response = {"user": user_serializer.data,
                        "colaborador": get_colaborador_serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
