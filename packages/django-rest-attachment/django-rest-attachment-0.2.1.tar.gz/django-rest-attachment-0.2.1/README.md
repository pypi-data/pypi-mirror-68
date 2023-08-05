# Django Rest Attachment

Django Free Attachment is a Django app to provide a simple attachment service independent of any other model. 

Detailed documentation is in the "docs" directory.

## Quick start


1. Setup environment
```bash
mkdir django
cd django
python -m venv .venv
source .venv/bin/activate

# Create requirements.txt file
cat <<EOF > requirements.txt
django<3,>=2.2
setuptools
djangorestframework
EOF

pip install -r requirements.txt
```

2.  Start Project

```bash
django-admin startproject proj
```

3.  Add "attachment" to your INSTALLED_APPS setting like this::

```python
    INSTALLED_APPS = [
        ...
        'rest_framework',
        'attachment',
    ]
```

3. Add Media settings, if you have done this, ignore this step

```python
MEDIA_DIR = os.path.join(BASE_DIR, "media")


MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
```

4. add routers.py to pro folder (the save folder with urls.py)

```python
# routers.py

from rest_framework import routers
from attachment.viewsets import AttachmentViewSet

router = routers.SimpleRouter()
router.register(r'attachment', AttachmentViewSet, basename='attachment')
```

5. Include the attachment and api URLconf in your project urls.py like this::

```python
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .routers import router

urlpatterns = [
  ....
  path('api/', include(router.urls), name='api'),
  path('attachment/', include('attachment.urls'), name='attachment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

6. Run ``python manage.py migrate`` to create the polls models.

7. Add superuser

```bash
python manage.py createsuperuser
python manage.py runserver
```

8. Start the development server and visit http://127.0.0.1:8000/admin/
   


## Test

1.  Visit http://127.0.0.1:8000/admin/attachment/ to upload a attachment from admin

2.  Using Postman to post a REST request:

-   add `X-CSRFToken` to header

-   add `session` id to Postman Cookies 

Postman can automatically extract session from chrome browser refer  [Postman Doc](https://learning.postman.com/docs/postman/sending-api-requests/capturing-http-requests/)

![image](https://i.imgur.com/n1HK4e5.png)

![images](https://i.imgur.com/gzI8T2i.png)