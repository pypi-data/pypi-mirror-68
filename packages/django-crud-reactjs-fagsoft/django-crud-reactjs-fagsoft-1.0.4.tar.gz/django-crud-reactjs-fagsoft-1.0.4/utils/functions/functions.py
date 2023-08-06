import base64
import operator
from functools import reduce
from django.conf import settings
from rest_framework import serializers
from Crypto.Cipher import AES
from django.db import models


def encrypt(texto_plano: str) -> str:
    if not texto_plano:  # pragma: no cover
        return ''
    key = settings.KEY_ENCRY
    vector = settings.VECTOR_ENCRY
    if len(key) not in [16, 24, 32]:  # pragma: no cover
        raise serializers.ValidationError('La contraseña debe ser de 16,24 o 32 caracteres')
    if len(vector) != 16:  # pragma: no cover
        raise serializers.ValidationError('El vector debe tener 16 caracteres')
    obj = AES.new(key, AES.MODE_CFB, vector)
    ciphertext = base64.b64encode(obj.encrypt(texto_plano)).decode("utf-8")
    return ciphertext.strip()


def decrypt(enc: str) -> str:
    if not enc:  # pragma: no cover
        return ''
    key = settings.KEY_ENCRY
    vector = settings.VECTOR_ENCRY
    if len(key) not in [16, 24, 32]:  # pragma: no cover
        raise serializers.ValidationError('La contraseña debe ser de 16,24 o 32 caracteres')
    if len(vector) != 16:  # pragma: no cover
        raise serializers.ValidationError('El vector debe tener 16 caracteres')
    obj2 = AES.new(key, AES.MODE_CFB, vector)
    decrypted_text = obj2.decrypt(base64.b64decode(enc)).decode("utf-8")
    return decrypted_text


def search_multiple_fields(queryset, search_fields, parameter):
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    orm_lookups = [construct_search(str(search_field))
                   for search_field in search_fields]
    for bit in parameter.split():
        or_queries = [models.Q(**{orm_lookup: bit})
                      for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries))
    return queryset
