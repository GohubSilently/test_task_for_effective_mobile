from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class DonationPermission(BasePermission):
    """
    anonymous → 401
    user      → POST
    moderator → GET
    admin     → всё
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False  # DRF сам вернёт 401

        role = getattr(user, "role", None)
        if not role:
            raise PermissionDenied()

        role = role.name

        if role == "admin":
            return True

        if request.method == "GET" and role == "moderator":
            return True

        if request.method == "POST" and role == "user":
            return True

        return False


class DonationMockView(APIView):
    permission_classes = [DonationPermission]

    def get(self, request):
        return Response(
            {"donations": ["donation-1", "donation-2"]},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        return Response(
            {"detail": "Donation created"},
            status=status.HTTP_201_CREATED
        )
