# coldfront-plugin-keycloak-usersearch

Keycloak user search plugin for ColdFront.

## Configuration

Set the following environment variables for the ColdFront deployment:

- `KEYCLOAK_URL`: Base URL for the Keycloak server
- `KEYCLOAK_REALM`: Realm used for both token issuance and user search
- `KEYCLOAK_CLIENT_ID`: Client ID for the service account used by this plugin
- `KEYCLOAK_CLIENT_SECRET`: Client secret for the service account used by this plugin

The plugin authenticates to Keycloak with the OAuth2 client credentials grant and then calls the Keycloak admin user search endpoints for the configured realm.

## Keycloak client setup

Create a dedicated confidential client in the same realm that ColdFront will search:

1. Create a new client in the target realm.
2. Enable **Client authentication**.
3. Enable **Service accounts roles**.
4. Copy the generated client ID and client secret into the ColdFront environment as `KEYCLOAK_CLIENT_ID` and `KEYCLOAK_CLIENT_SECRET`.

## Search-only permissions

Grant the service account only the permissions required to search and read users:

1. Open the client you created.
2. Go to **Service account roles**.
3. Select the `realm-management` client roles.
4. Assign `query-users` and `view-users`.

These roles allow the plugin to search users and read the fields returned by the Keycloak admin API without granting user-management permissions such as `manage-users`.
