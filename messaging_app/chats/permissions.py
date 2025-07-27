from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of the conversation for PUT, PATCH, DELETE requests.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, POST, etc.)
        if request.method not in ["PUT", "PATCH", "DELETE"]:
            return True

        conversation_id = view.kwargs.get('pk')  # assuming pk is used for conversation ID
        if not conversation_id:
            return False

        user = request.user
        return (
            user.is_authenticated and
            user.conversations.filter(id=conversation_id).exists()
        )
