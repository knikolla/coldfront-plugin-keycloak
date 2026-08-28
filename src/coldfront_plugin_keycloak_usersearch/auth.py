import logging

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from coldfront.core.utils.common import import_from_settings

logger = logging.getLogger(__name__)

PI_GROUP = import_from_settings("OIDC_PI_GROUP", "pi")
ADMIN_GROUP = import_from_settings("OIDC_ADMIN_GROUP", "coldfront-admins")


class OIDCKeycloakAuthenticationBackend(OIDCAuthenticationBackend):
    def get_username(self, claims):
        """Extract the username from the IdP payload."""
        # Check 'preferred_username' first (standard OIDC), falling back to 'username'
        # The overrides the default behavior of OIDCAuthenticationBackend which is to
        # hash the email address.
        return claims.get("preferred_username") or claims.get("username", "")

    def _sync_user(self, user, claims):
        """Syncs first name, last name, and admin permissions from claims."""
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")

        # Grant or revoke permissions based on group membership
        groups = claims.get("groups", [])

        is_pi = PI_GROUP in groups
        user.userprofile.is_pi = is_pi
        user.userprofile.save()

        is_admin = ADMIN_GROUP in groups
        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.save()

        return user

    def create_user(self, claims):
        """Called when a user logs in for the first time."""
        user = super().create_user(claims)
        return self._sync_user(user, claims)

    def update_user(self, user, claims):
        """Called on subsequent logins to keep permissions updated."""
        user = super().update_user(user, claims)
        return self._sync_user(user, claims)
