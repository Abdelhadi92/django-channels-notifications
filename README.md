# Django Channels Notifications
Notifying users of various things that happen in your application is super easy to implement. Django Channels notifications allow you to send a message to any user via Email, Datbase, and many other channels.

<br/>

## Installation

1. Run the [pip](https://pip.pypa.io/en/stable/) command to install the latest version:

```bash
 pip install django-channels-notifications
```

2. Add `django_channels_notifications` to your `INSTALLED_APPS` in settings.py:
```bash
 INSTALLED_APPS = (
    ...
    'django_channels_notifications',
 )
```

3. Run the migration command:
```bash
 python manage.py migrate
```

<br/>

## Creating Notifications

In Django Channels Notifications, each notification is represented by a single class, and to create a new notification you can run the following manage.py command:
```bash
 python manage.py createnotification TestNotification
 ```   
 
And this will place a fresh notification class with the below contents. Each notification class contains a `via` method and a variable number of message building methods (such as `to_mail` or `to_database`) that convert the notification to a message optimized for that particular channel.

```python
from django_channels_notifications.core import Notification  
from django_channels_notifications.core.channels import DatabaseChannel  
  
  
class TestNotification(Notification):  
  
  # Get the notification's delivery channels.  
  def via(self, notifiable):  
        return [DatabaseChannel]  
  
  # Get the dict representation of the notification.  
  def to_database(self, notifiable):  
        pass
```
<br/>

## Sending  Notifications

###  # Using The Notifiable Mixin
Notifications may be sent in two ways: using the notify method of the Notifiable mixin or using the NotificationSender . First, let's explore using the mixin:

```python
 from django_channels_notifications.core import Notifiable
 from django.db import models

 class Profile(models.Model, Notifiable):  
	phone = models.CharField(max_length=255, verbose_name='Phone')
	address = models.TextField(max_length=512,verbose_name='Address')
	
```
Adding `Notifiable` mixin in your  `Profile` model will allow you to easily send notifications to profiles using `notify` method. The `notify` method expects to receive a notification instance:
```python
 profile = Profile.objects.get(pk=1)
 profile.notify(TestNotification());
```

**Remember ,** you may use the `django_channels_notifications.core.Notifiable` mixin on any of your models. You are not limited to only including it on your `Profile`model.


###  # Using The NotificationSender:
Alternatively, you may send notifications via the `NotificationSender` . This is useful primarily when you need to send a notification to multiple notifiable entities such as a list of profiles. To send notifications using the NotificationSender, pass all of the notifiable entities and the notification instance to the `send` method:

```python
 from django_channels_notifications.core import NotificationSender
 
 profiles = Profile.objects.all()
 NotificationSender.send(profiles, TestNotification())
 
```

###  # Specifying Delivery Channels:
Every notification class has a `via` method that determines on which channels the notification will be delivered. Notifications may be sent on the `database`, `mail`,  `unifonc` channels.

The `via` method receives a `notifiable` instance, which will be an instance of the class to which the notification is being sent. You may use `notifiable` to determine which channels the notification should be delivered on:

```python

 #Get the notification's delivery channels.
 def via(self, notifiable):
	 if notifiable.prefers_sms:
		return [UnifonicChannel]
	 return	[DatabaseChannel]
	 	     
```
Let's quickly go through the different notification channels supported by Django Channels Notifications.

-   **Database:** This option allows you to store notifications in a database should you wish to build a custom UI to display it.
-  **Mail:** The notifications will be sent in the form of email to users.
-  **Unifonic:** As the name suggests, users will receive SMS notifications on their phone.
<br/>

## Database Channel
The `DatabaseChannel` notification stores the notification information in a database table. This table will contain information such as the notification type as well as custom JSON data that describes the notification.

###  # Formatting Database Notifications:
If a notification supports being stored in a database table, you should define a `to_database`  method on the notification class. This method will receive a `notifiable` entity and should return a plain Python dict. The returned dict will be encoded as JSON and stored in the `data` column of your `notifications` table. Let's take a look at an example `to_database` method:

```python

 # Get the dict representation of the notification. 
 def to_database(self, notifiable): 
    return {
        'invoice_id': 12,
        'amount': 200,
    } 
    
```

###  # Accessing The Notifications
Once notifications are stored in the database, you need a convenient way to access them from your notifiable entities. To fetch notifications, you may use the `notifications` method. By default, notifications will be sorted by the `created_at` timestamp:
```python

 profile = Profile.objects.get(pk=1)
 
 for notification in profile.notifications():
     print(notification.type)

```

If you want to retrieve only the "unread" notifications, you may use the  `unread_notifications`  method and If you want to retrieve only the "read" notifications, you may use the  `read_notifications`  method. Again, these notifications will be sorted by the  `created_at`  timestamp:

```python

 profile = Profile.objects.get(pk=1)
 
 for notification in profile.unread_notifications():
     print(notification.type)
     
 for notification in profile.read_notifications():
     print(notification.type)
```

###  # Marking Notifications As Read , Unread: 
Typically, you will want to mark a notification as "read" when a user views it. The `django_channels_notifications.core.notifiable` mixin provides  `mark_as_read` and `mark_as_unread` methods, which updates the `read_at` column on the notification's database record:

```python

profile = Profile.objects.get(pk=1)

# Marking notifications as read
for notification in profile.unread_notifications():
    notification.mark_as_read()
    
# Marking notifications as unread   
for notification in profile.read_notifications():
    notification.mark_as_unread()    
    
```
<br/>

## Mail Channel  
If a notification supports being sent as an email, you should define a `to_mail` method on the notification class. This method will receive a `notifiable` entity and should return a [`django.core.mail.EmailMessage`](https://docs.djangoproject.com/en/2.2/topics/email/#the-emailmessage-class)  or  [`django.core.mail.EmailMultiAlternatives`](https://docs.djangoproject.com/en/2.2/topics/email/#sending-alternative-content-types) instance. Let's take a look at an example `to_mail` method:   
```python
from django.core.mail import EmailMessage
 
 # Get the mail representation of the notification.
 def to_mail(self, notifiable):  
    return EmailMessage(
        'Hello',
        'Body goes here',
        'from@example.com',
        ['to1@example.com', 'to2@example.com'],
        ['bcc@example.com'],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},
    )    

```

###  # Sending through "Mailgun" :
To use the Mailgun provider,  you need to add the following parameters to your `settings.py`:

```bash
 EMAIL_HOST = 'smtp.mailgun.org'  
 EMAIL_PORT = 587  
 EMAIL_HOST_USER = 'postmaster@msg.com' #please change this with your username  
 EMAIL_HOST_PASSWORD = '112233445566778899' #please change this with your password  
 EMAIL_USE_TLS  =  True
```

###  # Sending through "SES" :
To use the SES provider, you'll need [Boto](http://boto.cloudhackers.com/) 2.1.0 or higher. [Boto](http://boto.cloudhackers.com/) is a Python library that wraps the AWS API. 

You can do the following to install boto 2.1.0 (we're using --upgrade here to make sure you get 2.1.0):
```bash
pip install --upgrade boto
```

Install django-ses:
```bash
pip install django-ses
```

Add the following to your settings.py:

```python
EMAIL_BACKEND = 'django_ses.SESBackend'

# These are optional -- if they're set as environment variables they won't
# need to be set here as well
AWS_ACCESS_KEY_ID = 'YOUR-ACCESS-KEY-ID'
AWS_SECRET_ACCESS_KEY = 'YOUR-SECRET-ACCESS-KEY'

# Additionally, if you are not using the default AWS region of us-east-1,
# you need to specify a region, like so:
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
```

<br/>

## Unifonic Channel
The `UnifonicChannel` notification allow you to sent the notification as SMS via Unifonic.

You need to add `UNIFONIC_APPSID`  in settings.py:
```bash
 UNIFONIC_APPSID = "Your Unifonic APPSID" 
```


###  # Formatting Unifonic Notifications:
If a notification supports being sent as an SMS, you should define a `to_unifonic` method on the notification class. This method will receive a `notifiable` entity and should return a `django_channels_notifications.core.channels.unifonic_channel.UnifonicMessage` instance:
```python
 from django_channels_notifications.core.channels.unifonic_channel import UnifonicMessage
 
 # Get the Unifonic representation of the notification.
 def to_unifonic(self, notifiable):  
    return UnifonicMessage().set_body('Your SMS message content').set_recipient(notifiable.phone)
    
```
### # Customizing The "SenderID":
If you would like to send some notifications from a SenderID that is different from the default SenderID in your  Unifonic account, you may use the  `set_sender_id` method on a  `UnifonicMessage`  instance:
```python
 from django_channels_notifications.core.channels.unifonic_channel import UnifonicMessage
 
 # Get the Unifonic representation of the notification.
 def to_unifonic(self, notifiable):  
    return UnifonicMessage().set_body('Your SMS message content').set_recipient(notifiable.phone).set_sender_id('Your SenderID')
    
```
<br/>

## Custom Channels
Django Channels Notifications ships with a handful of notification channels, but you may want to write your own channel to deliver notifications via other channels. Django Channels Notifications makes it simple. To get started, define a class that extended from `django_channels_notifications.core.BaseChannel` and contains a `send` method. The method should receive two arguments: a `notifiable` and a `notification`. or by run the following manage.py command:

```bash
 python manage.py createchannel TestChannel
```

```python
 from django_channels_notifications.core import BaseChannel  
  
  
 class TestChannel(BaseChannel):  
	# Send the given notification.  
	def send(self, notifiable, notification):  
        pass
	 	     
```
Once your notification channel class has been defined, you may return the class name from the `via` method of any of your notifications:

```python
class TestNotification(Notification):  
  
  # Get the notification's delivery channels.  
  def via(self, notifiable):  
        return [DatabaseChannel, TestChannel]  
  
  # Get the dict representation of the notification.  
  def to_database(self, notifiable):  
        pass
        
  # Get the dict representation of the notification.  
  def to_test(self, notifiable):  
        pass
```
