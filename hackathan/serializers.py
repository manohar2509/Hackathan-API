from rest_framework import serializers
from .models import Hackathon, Registration, Submission

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

        # make image_submission and file_submission and link_submission optional
        extra_kwargs = {
            'image_submission': {'required': False, 'allow_null': True},
            'file_submission': {'required': False, 'allow_null': True},
            'link_submission': {'required': False, 'allow_null': True},
        }
            
