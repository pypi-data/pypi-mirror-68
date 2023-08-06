# Local Yinxiang access to Yinxiang server

## Principal



This app has the following responsibilities:
1. Pull account/tag/note/notebook data from Yinxiang API
2. Push changes to Yinxiang API





## How to use it



Install from Pypi

```
pip install -U django_yx_app
```

Modify `settings.py`

1. add evernote key settings 
    ```
    EVERNOTE_CONSUMER_KEY='axplus****'
    EVERNOTE_CONSUMER_SECRET='****'
    EVERNOTE_SERVICE_HOST='app.yinxiang.com' # or 'sandbox.yinxiang.com'
    ```
2. add to `INSTALLED_APPS`
    ```
    INSTALLED_APPS=[
        ...
        'yx'
    ]
    ```


