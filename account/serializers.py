from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password', 'password1']

        extra_kwargs = {
            'password': {'write_only':True},
            'password1': {'write_only':True}
        }

    def create(self, validate_data):
        passw = validate_data['password']
        passw2 = validate_data['password1']
        if passw != passw2:
            raise serializers.ValidationError({'error': 'Password fields do not match.'})
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance