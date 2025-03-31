# accounts/serializers.py
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Add a basic CharField to satisfy the check
    test_field = serializers.CharField()
    
    # Explicitly declared fields
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        # Ensure 'password' and 'password2' are included in this list
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'password', 'password2', 'test_field')
        read_only_fields = ('id',) # id is implicitly read-only on create anyway

    def validate(self, attrs):
        # Check that the two password entries match
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 as we don't need it for user creation
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        
        # Create user using create_user method
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            **{k: v for k, v in validated_data.items() if k not in ['username', 'email']}
        )
        user.set_password(password)
        user.save()
        
        # Create token for the user
        Token.objects.create(user=user)
        
        return user

# --- ProfileSerializer remains the same ---
class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing/updating user profile (excludes password)"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        read_only_fields = ('id', 'username', 'email')