# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    # Explicitly declared fields
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = CustomUser
        # Ensure 'password' and 'password2' are included in this list
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'password', 'password2')
        read_only_fields = ('id',) # id is implicitly read-only on create anyway

    def validate(self, attrs):
        # Check that the two password entries match
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Create the user instance
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', None),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Hash the password
        user.set_password(validated_data['password'])
        user.save()
        return user

# --- ProfileSerializer likely remains the same ---
class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing/updating user profile (excludes password)"""
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        read_only_fields = ('id', 'username', 'email')