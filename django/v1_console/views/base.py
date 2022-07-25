from rest_framework import views
from v1_console.authentication import CognitoAuthentication
from v1_console.permissions import IsAuthenticated


class ConsoleBaseView(views.APIView):
    """
    Base authentication class applying for console app.
    Any Console view class should be inherited this base to using CognitoAuthentication
    """
    authentication_classes = (CognitoAuthentication,)
    permission_classes = (IsAuthenticated,)
