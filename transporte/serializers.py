from rest_framework import serializers
from . import models


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = models.Usuario
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
                  'email', 'rol', 'telefono')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = models.Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        else:
            usuario.set_unusable_password()
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conductor
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vehiculo
        fields = '__all__'


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ruta
        fields = '__all__'


class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Viaje
        fields = '__all__'


class HistorialEstadoViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistorialEstadoViaje
        fields = '__all__'


class IncidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Incidencia
        fields = '__all__'