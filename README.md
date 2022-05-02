# User Login System using JWT

This login system saves the user from entering the credentials less frequently without losing the privacy of the user.

## How it works ?

**New User (Sign Up)**

* If the username is available
    * Saves the username and the hashed version of the chosen password into the database

**Existing User (Login)**
* If the credentials are valid
    * A fresh access token is generated and stored in an cookie

    (After Every Request)
    * The expiry time of the access token is verified
        * If the expiry time is found to be in the next 10 min (this time interval can be modified to suit the needs)
            * New access token (not fresh) is generated and replaces the existing token

    (Fresh Access Token)
    * If the user has a fresh token (i.e. within the first 30 min (this time interval can be modified to suit the needs) after entering the credentials)
        * User acess to the API resources is not limited
    
    (Not Fresh Access Token)
    * If the user's access token is not fresh ((i.e. 30 min (this time interval can be modified to suit the needs) after entering the credentials))
        * User access to the API resources is limited
        * If the user wants to access more secure API resources
            * The user must verify his/her identity by re-entering the credentials which creates a new fresh access token 
