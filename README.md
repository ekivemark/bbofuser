Developer Account Framework
===========================

This is the second iteration of a Developer Account Framework. 
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



