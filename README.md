[![Downloads](https://static.pepy.tech/personalized-badge/ninja-put-patch-file-upload-middleware?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/ninja-put-patch-file-upload-middleware)

# ninja_put_patch_file_upload_middleware
This middleware allows users to upload files using the HTTP PUT or PATCH method. Backports the functionality from [django-ninja#719](https://github.com/vitalik/django-ninja/pull/719) which in turn is based on  [django-ninja#417 (comment)](https://github.com/vitalik/django-ninja/issues/417#issuecomment-1092545699) which should be available in `django-ninja` if [django-ninja#397](https://github.com/vitalik/django-ninja/pull/397) is merged ( in that case this middleware works as a backport )

## Requirements

* Django 3.2+ 
* Asgiref 3.6.0+
* Python 3.9+

## Installation

1. Install the package using pip :
```bash
pip install ninja_put_patch_file_upload_middleware
```
2. Add the middleware to your middleware stack:

```python
# settings.py

MIDDLEWARE = [
    ...
    "ninja_put_patch_file_upload_middleware.middlewares.process_put_patch",
]
```


## LICENSE

This package is licensed under the MIT License ( same as `django-ninja` ). See the [LICENSE](https://github.com/baseplate-admin/ninja_put_patch_file_upload_middleware/blob/master/LICENSE) file for more information.


## Feature Complete

I am not willing to add any more functionality to this module. This should work as is. Unless there are changes in `django`/`asgiref` side. Please dont ask for changes >_<
