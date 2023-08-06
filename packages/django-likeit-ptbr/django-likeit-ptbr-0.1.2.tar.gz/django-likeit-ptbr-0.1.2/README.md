# django-likeit-ptbr
A simple app for Django that enables users to like and unlike any object/item within any model.
It's developed on Python 3.5 & Python 3.6 for Django 2.0 and later. Adjustments made from original django-likeit

## Installation


* Install django-likeit in your vilrtual env:

```
pip install django-likeit-ptbr
```

* Add the app to your settings.py

```python
INSTALLED_APPS = [
  ...
  "like",
  ...
]
```

* Add likeit urls to your project's `urls.py` file:

```python
from django.conf.urls import url, include

urlpatterns = [
  ...
  url(r'^like/', include('like.urls')),
  ...
]
```

* Migrations:

```
python manage.py makemigrations like
python manage.py migrate
```

* Make sure you have jQuery ajax CSRF configuration right, and also you included Font Awesome in your HTML.

## Usage:


### Template tags:

* Get the liked objects for a given user:

```python
{% with user_likes <user> "app_label.model" as like_list %}
    {% for like_obj in like_list %}
        {# do something with like_obj #}
    {% endfor %}
{% endwith %}
```


* Given an object `obj` you may show it like count like this:

```python
<p>Like Count {{ obj|likes_count }}</p>
```


* Get Like instance for an object (obj) and a user (user)

```python
{% with obj|get_like_for:user as like_object %}
    ...
{% endwith %}
```

* Like Button for an object `my_obj`:

```python
{% like_button my_obj %}
```


### Likes Manager

* Create a Like instance for a user and object:

```python
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='jdoe')
>>> song = Song.objects.get(pk=1)
>>> like = Like.objects.create(user, song)
```

    or:

```python
>>> like = Like.objects.create(user, 1, Song)
```

    or:

```python
>>> like = Like.objects.create(user, 1, "music.Song")
```

 * Get the objects liked by a given user:

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='jdoe')
>>> Like.objects.for_user(user)
>>> [<Like: Like object 1>, <Like: Like object 2>, <Like: Like object 3>]
```

* Now, get user liked objects belonging to a given model:

```python
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='jdoe')
>>> Like.objects.for_user(user, model=Song)
>>> [<Like: Like object 1>, <Like: Like object 2>, <Like: Like object 3>]
```

* Get the liked object instances of a given model liked by any user:

```python
>>> from music.models import Song
>>> Like.objects.for_model(Song)
>>> [<Like: Like object 1>, <Like: Like object 2>, <Like: Like object 3>]
```

* Get a Like instance for a given object and user:

```python
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='jdoe')
>>> song = Song.objects.get(pk=1)
>>> like = Like.objects.get_like(user, song)
```

* Get all Like instances for a given object

```python
>>> from music.models import Song
>>> song = Song.objects.get(pk=1)
>>> like = Like.objects.for_object(song)
```
