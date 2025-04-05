from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    target_type = serializers.ReadOnlyField(source='target_content_type.model')
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_type', 'target_object_id', 
                 'created_at', 'is_read']
        read_only_fields = ['created_at']