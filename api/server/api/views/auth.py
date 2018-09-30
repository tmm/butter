from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..lib import PlaidClient
from ..models import Account, Institution, Item
from ..serializers import LinkPlaidSerializer, LoginSerializer, RegisterSerializer

plaid = PlaidClient()
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password", "password_confirm", "public_token")
)


class LinkPlaidView(GenericAPIView):
    """
    API endpoint that adds an account after using Plaid Link
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LinkPlaidSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LinkPlaidView, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        institution_data = serializer.validated_data["institution"]
        institution, _ = Institution.objects.get_or_create(
            institution_id=institution_data.get("institution_id"),
            name=institution_data.get("name"),
        )

        user = request.auth.user
        public_token = serializer.validated_data["token"]
        access_token, item_id = plaid.get_access_token(public_token)
        item = Item.objects.create(
            access_token=access_token,
            item_id=item_id,
            user=user,
            institution=institution,
        )

        accounts = serializer.validated_data["accounts"]
        for account in accounts:
            Account.objects.create(
                account_id=account.get("account_id"),
                mask=account.get("mask"),
                name=account.get("name"),
                subtype=account.get("subtype"),
                type=account.get("type"),
                user=user,
                institution=institution,
                item=item,
            )
        return Response({}, status=status.HTTP_200_OK, headers={})


class LoginView(GenericAPIView):
    """
    API endpoint that allows an user to login
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return {"id": user.pk, "email": user.email, "token": token.key}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            self.get_response_data(user), status=status.HTTP_200_OK, headers={}
        )


class LogoutView(APIView):
    """
    API endpoint that allows an user to logout
    """

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        response = self.http_method_not_allowed(request, *args, **kwargs)
        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Response(
            {"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK
        )


class RegisterView(CreateAPIView):
    """
    API endpoint that allows an user to register
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return {"id": user.pk, "email": user.email, "token": token.key}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )