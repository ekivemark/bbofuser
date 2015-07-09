Developer Account Framework (3)
===========================

This is the third iteration of a Developer Account Framework. 

The big change here is the port to Python 3.4.3. 

The objective is to create a platform that allows Developers to: 

- sign up for an account
- Validate their account via email
- Agree to Terms of Use
- Manage their account
- Manage OAuth Credentials

This version implements a Custom User model that uses email as username.
Django-registration-redux is also implemented to issue email to complete 
registration. This required some overrides to use email and not username.

The custom user model is in accounts.

The custom user model also implements multi-factor authentication. 
This uses telephone and carrier information in the User model to send
a 4-digit code to the cell phone of the user as part of the login process.

This version also uses email as the account id through a custom user model.
The accounts app also implements multi-factor authentication using email 
sent to the accounts registered mobile phone,if MFA is set to true in the
profile.

The SMS routines require the user to pick a carrier identity. The app then
uses email/smtp to send a 4-digit code to the user. This takes advantage of
most (all) carriers having an email to SMS gateway.
