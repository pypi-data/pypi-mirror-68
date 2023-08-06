from django.core.exceptions import ObjectDoesNotExist


def update_or_create(model_manager, defaults=None, **kwargs):
    defaults = defaults or {}
    try:
        instance = model_manager.get(**kwargs)
        for k, v in defaults.items():
            setattr(instance, k, v)
        instance.save()
        return instance, False
    except ObjectDoesNotExist:
        defaults.update(kwargs)
        instance = model_manager.create(**defaults)
        return instance, True
