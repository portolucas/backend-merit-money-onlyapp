from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import Cargo, Setor, Premios, Transacao, TransacaoPremios, Colaborador


class CargoSerializer(serializers.ModelSerializer):
    cargo_colaborador = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Cargo
        fields = ('id', 'descricao', 'cargo_colaborador')


class SetorSerializer(serializers.ModelSerializer):
    setor_colaborador = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Setor
        fields = ('id', 'descricao', 'setor_colaborador')


class PremiosSerializer(serializers.ModelSerializer):
    premios_colaborador = serializers.StringRelatedField(
        many=True, read_only=True, required=False)

    class Meta:
        model = Premios
        fields = ('id', 'descricao', 'valor', 'premios_colaborador')


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ('id', 'data_transacao', 'id_remetente',
                  'id_destinatario', 'valor', 'justificativa')


class TransacaoPremiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransacaoPremios
        fields = ('id', 'data_transacao', 'premio_resgatado', 'id_colaborador')


class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ('id', 'nome', 'sobrenome', 'cargo', 'setor',
                  'saldo_acumulado', 'saldo_recebido', 'premios')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
