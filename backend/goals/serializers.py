from rest_framework import serializers
from .models import Goal
from tasks.serializers import TaskSerializers

class GoalSerializer(serializers.ModelSerializer):
    tasks = TaskSerializers(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'due_date', 'tasks']
