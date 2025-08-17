from rest_framework import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    For PUT, PATCH, DELETE methods, only participants are allowed.
    """
    def has_permission(self, request, view):
        conversation_id = view.kwargs.get('pk')
        if not conversation_id:
            return False
        
        user = request.user
        is_participant = user.is_authenticated and user.conversations.filter(conversation_id=conversation_id).exists()
        
        # Only allow PUT, PATCH, DELETE for participants
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant
        # For other methods, keep the original logic (e.g., GET, POST)
        return is_participant