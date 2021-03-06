from rest_framework import serializers

from .models import Emoji


class EmojiSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that maps all of the Emoji model fields with the given
    serializer fields of ``id``, ``uuid``, ``emoji``, ``name``, ``slug``,
    ``created_at``, and ``updated_at``.

    NOTE: All Django models have an ``id`` field by default upon creation.
    """

    class Meta:
        model = Emoji
        fields = (
            "id",
            "uuid",
            "emoji",
            "name",
            "slug",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["createdAt"] = representation["created_at"]
        representation["updatedAt"] = representation["updated_at"]

        representation.pop("created_at")
        representation.pop("updated_at")

        return representation
