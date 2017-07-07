# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.core.validators import BaseValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from strategy_field.fields import ClassnameValidator
from strategy_field.utils import import_by_name, fqn

logger = logging.getLogger(__name__)

class RegistryValidator(BaseValidator):

    def __call__(self, value):
        if not self.limit_value.is_valid(value):
            raise ValidationError("Invalid entry")


class DrfStrategyField(serializers.ChoiceField):
    default_validators = [ClassnameValidator]

    def __init__(self, registry, **kwargs):
        choices = registry.as_choices()
        super(DrfStrategyField, self).__init__(choices, **kwargs)
        self.registry = registry

    def get_validators(self):
        ret = super().get_validators()
        ret.append(RegistryValidator(self.registry))
        return ret

    def to_representation(self, obj):
        return fqn(obj)

    def to_internal_value(self, data):
        return data


class DrfMultipleStrategyField(serializers.ChoiceField):
    default_validators = [ClassnameValidator]

    def __init__(self, registry, **kwargs):
        choices = registry.as_choices()
        super(DrfMultipleStrategyField, self).__init__(choices, **kwargs)
        self.registry = registry

    def to_representation(self, obj):
        return [fqn(i) for i in obj]

    def to_internal_value(self, data):
        return [import_by_name(i) for i in data]

    def run_validators(self, value):
        return super(DrfMultipleStrategyField, self).run_validators(value)