from rest_framework import generics, permissions

import api.serializers as serializers

class UserDetail(generics.RetrieveAPIView):
    """ Get a list of events for the current organisation. """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user