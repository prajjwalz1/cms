
from rest_framework import serializers
from .models import *
class WorkflowSerializer(serializers.ModelSerializer):
    request_from_type = serializers.CharField(source='request_from_type.model')
    request_dest_type = serializers.CharField(source='request_dest_type.model', allow_null=True)


    class Meta:
        model = Workflow
        fields = ['id','request_item', 'request_from_type', 'request_dest_type','status']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        request_from_instance = instance.request_from
        if request_from_instance:
            ret['request_from'] = str(request_from_instance)
        else:
            ret['request_from'] = None

        request_dest_instance = instance.request_dest
        if request_dest_instance:
            ret['request_dest'] = str(request_dest_instance)
        else:
            ret['request_dest'] = None
        
        return ret
