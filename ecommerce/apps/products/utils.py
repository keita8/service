from django.utils.text import slugify
import random
import string


def random_string_generator(size=5, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):

    new_order_id = random_string_generator().upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(reference=new_order_id).exists()

    if qs_exists:
        return unique_slug_generator(instance)

    return new_order_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        reference = new_slug
    else:
        slug = slugify(instance.product_id)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(reference=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(reference=slug, randstr=random_string_generator(size=10))
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug
