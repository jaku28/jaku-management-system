from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import exceptions, serializers
from . import models


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, validated_data):
        new_password = validated_data['new_password']
        new_password2 = validated_data['new_password2']
        if new_password != new_password2:
            raise serializers.ValidationError('Las contraseñas no coinciden.')

        return validated_data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
            model = models.Profile
            fields = ('phone', 'avatar')


class UserSerializer(serializers.ModelSerializer):    
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile',)        

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        # Validate email is not already in use.
        email = validated_data['email']
        if User.objects.filter(email=email).exists():
            raise exceptions.ValidationError(
                {'email': [_('A user with that email already exists.')]})
        
        profile = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        user.profile.__dict__.update(profile)
        user.profile.save()
        
        return user

    def update(self, instance, validated_data):
        if self.context['request'].user == instance:            
            profile = validated_data.pop('profile')            
            instance.__dict__.update(**validated_data)
            instance.save()

            instance.profile.__dict__.update(profile)            
            instance.profile.save()

            return instance
            
        else:
            raise Http404

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    default_error_messages = {
        'invalid_password': 'old password does not match'
    }
