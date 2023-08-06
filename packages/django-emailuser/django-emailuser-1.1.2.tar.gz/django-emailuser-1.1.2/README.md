
# # `emailuser` is a Django Custom User Module

#Package Version: 1.x
`emailuser` makes it easy to use email address as your identification token instead of a username.
emailuser is a custom Django user model (extends  `AbstractBaseUser`) so it takes a tiny amount of effort to use.

The only difference between emailuser and the vanilla Django  `User`  is email address is the  `USERNAME_FIELD`  (and username also exist, If you not give it in `create_user` it will generate a `random 12 char unique string as username`).

emailuser supports Django 2.* to 3.*
# When to use emailuser ?

When you need email as username in django project.

# Why I have created emailuser?

I have created this custom user package for my university final project where I need to create user using university email also all user must have a profile link using unique username.

I think this package can help me in other application development also it can help other people too. That is why I published it.
If you love it you can [donate](https://commerce.coinbase.com/checkout/c3eafb3c-65ba-40b5-b555-2037989de629).

# Install and setup

 1. Install with `pip`:
  ```
    #Django 2.x, or 3.x

    pip install django-emailuser 
  ```
 2. Add `emailuser` to your `INSTALLED_APPS` setting:
 
  ```  
    
    INSTALLED_APPS = [
        ...
        'emailuser',
    ]
    
  ```
 3. Specify the custom model as the default user model for your project using the `AUTH_USER_MODEL` setting in your setting:
 
  ```
    AUTH_USER_MODEL = "emailuser.User"
  ```
 5. Run migrations (Don't do any migrate before `emailuser` makemigrations).
 
   if you have tables referencing Django  `User`  model, you will have to delete those table and migrations, then re-migrate. This will ensure everything is set up correctly from the beginning.
  
   ```
    python manage.py makemigrations emailuser
    python manage.py migrate
  ```

 6. Instead of referring to User directly, you should reference the user model using  `django.contrib.auth.get_user_model()`

  When you define a foreign key or many-to-many relations to the  `User`  model, you should specify the custom model using the  `AUTH_USER_MODEL`  setting.

  ```
  from django.conf import settings
  from django.db import models

  class Profile(models.Model):
      user = models.ForeignKey(
          settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE,
  )
  ```
7: For Django Rest Framework

    from django.contrib.auth import get_user_model
    class  UserSerializer(serializers.ModelSerializer):
      class  Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name')

 8: Helper Functions
  

    from django.contrib.auth import get_user_model
    
    get_user_model().objects.get_full_name()  # Return Full Name
    
    /*
    For sending email you must configure smtp setting like below
      EMAIL_HOST = 'hostname'
    EMAIL_PORT = port
    EMAIL_HOST_USER = 'username'
    EMAIL_HOST_PASSWORD = 'password'
    EMAIL_USE_TLS = True
  */
  
    get_user_model().objects.send_email(subject, message, from_email)   
  
  # this will send email to logged in user
  # by default it will not show sending error 
  # for showing error extra False argument required like below
  
  get_user_model().objects.send_email(subject, message, from_email, False)  

9: Registraion

    get_user_model().objects.create_user(email, password, first_name, last_name, username)
    #username field is optional. If it's empty a rendom unique username will be created
    
10: Login

    #Required argument
    email and password

Note. FOO@example.com will be replaced to foo@example.com automatically

 
## License

Released under the MIT license. See [LICENSE](https://github.com/Swe-HimelRana/django-email-user/blob/master/LICENSE) for details.

## [](https://github.com/Swe-HimelRana/django-email-user#questions-comments-or-anything-else)Questions, comments, or anything else?
-   [Contribute](https://github.com/Swe-HimelRana/django-email-user/)
-   [Open an issue](https://github.com/Swe-HimelRana/django-email-user/issues)
-   [https://www.linkedin.com/in/swe-himelrana](https://www.linkedin.com/in/swe-himelrana)
-   [contact@himelrana-swe.com](mailto:contact@himelrana-swe.com)
 
 Give a thanks by [Donation](https://commerce.coinbase.com/checkout/c3eafb3c-65ba-40b5-b555-2037989de629)
 