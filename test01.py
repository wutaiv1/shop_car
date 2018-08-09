import os

if __name__ == "__main__":
    # 下面os.environ.setdefault 来自启动程序：manage.py
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lfctity.settings")

    # django.setup 是从来启动Django 的配置
    import django

    django.setup()

    from api import models
    import datetime

    ret =  models.Course.objects.all().values("name","price_policy")
    print(ret)