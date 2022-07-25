from rest_framework import serializers
from database.models import Terminal


class TerminalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = "__all__"

    def create(self, validated_data):
        terminal = Terminal(
        )
        terminal.save()
        return terminal
