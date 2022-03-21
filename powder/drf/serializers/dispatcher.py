from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypedDict

if TYPE_CHECKING:
    from rest_framework import serializers
    from rest_framework import views


class _SerializerGetter:
    def __init__(self, default: serializers.Serializer, **kwargs):
        self.default = default
        self.serializer_per_action = kwargs

    def get_serializer_class(self, view: views.APIView) -> Type[serializers.Serializer]:
        return self.serializer_per_action.get(
            getattr(view, 'action', None),
            self.default
        )

    def __call__(self, *args, **kwargs) -> serializers.Serializer:
        context = kwargs.get('context', {})
        view: Optional[views.APIView] = context.get('view', None)
        serializer_class = self.get_serializer_class(view)
        return serializer_class(*args, **kwargs)


class SerializerDispatcher:
    def __init__(self, default, **kwargs):
        self.serializer_getter = _SerializerGetter(
            default=default, **kwargs,
        )

    def __call__(self, *args, **kwargs):
        return self.serializer_getter(*args, **kwargs)
