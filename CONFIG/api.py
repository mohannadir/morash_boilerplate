# The API uses JWT for authentication. The following settings are used to configure the JWT tokens.

# This should be a secret key different from the one used in the Django settings. You can generate one here: https://djecrety.ir/
SIGNING_KEY = 'zs_*m$&@i3o2z62kq%=1-9^+me3qxyu_&1=qzwqqsa7jyjre@%' 

# The access token expiral in minutes. The user has to get a new access token after the access token expires.
# This can be by logging in again or using the refresh token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# The refresh token expiral in days. The user can use the refresh token to get a new access token after the access token expires. The refresh token expires after 30 days.
# If the user's access token has expired and the user has a valid refresh token, the user can use the refresh token to get a new access token without having to log in again.
# Otherwise, if the access token and refresh token have expired, the user has to log in again.
REFRESH_TOKEN_EXPIRES_DAYS = 30