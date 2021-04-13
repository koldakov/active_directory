# Copyright (c) 2021, Ivan Koldakov.
# All rights not reserved.
#
# Use as you want, modify as you want but please include the author's name.

"""
Util for admin actions.
This util can (should) be moved to global utils due to independence code style.
"""

import csv
import datetime
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.core import exceptions
from django.http import StreamingHttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from itertools import chain


class Echo(object):
    """ Pseudo buffer class
    """
    def write(self, value):
        return value


def change_fields(modeladmin, request, queryset):
    if request.POST.get('post'):
        fields = request.POST.get('fields', {})

        if fields and isinstance(fields, dict):
            msg = _(f'Error: Unknown error')
            try:
                queryset.update(**fields)
                msg = _(f'Fields {", ".join(fields.keys())} updated successfully')
            except (exceptions.FieldDoesNotExist,
                    exceptions.FieldError,
                    exceptions.PermissionDenied,
                    exceptions.TooManyFieldsSent,
                    ValueError, TypeError) as e:
                msg = _(f'Do not try to hack me.')
            finally:
                modeladmin.message_user(request, msg)
        return None

    opts = modeladmin.opts
    objects_name = model_ngettext(queryset)
    title = _(f'Change multiple fields in {objects_name} objects')

    context = {
        **modeladmin.admin_site.each_context(request),
        'title': title,
        'queryset': queryset,
        'perms_lacking': [],
        'opts': opts,
        'objects_name': objects_name,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'media': modeladmin.media,
    }

    request.current_app = modeladmin.admin_site.name
    return TemplateResponse(
        request, "admin/admin_actions/change_fields_confirmation.html", context)


change_fields.short_description = _('Change values in multiple fields')
change_fields.allowed_permissions = ['change']


def get_csv(modeladmin, request, queryset):
    """
    TODO check OOM on big data
    """
    opts = modeladmin.opts

    if request.POST.get('post'):
        field_names = tuple(
            [field.name for field in opts.fields if field.name not in 'password' or not request.user.is_superuser])

        # TODO time format dependency on language
        time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        filename = f'{opts}_{time_now}.csv'

        # Generate streaming response
        pseudo_buffer = Echo()
        streaming_writer = csv.writer(pseudo_buffer, delimiter=',')
        pseudo_buffer.write(field_names)
        response = StreamingHttpResponse(
            (streaming_writer.writerow(row) for row in chain([field_names], [
                [getattr(obj, field) for field in field_names] for obj in queryset
            ])),
            content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    objects_name = model_ngettext(queryset)
    title = _(f'Get CSV from {objects_name} objects')

    context = {
        **modeladmin.admin_site.each_context(request),
        'title': title,
        'queryset': queryset,
        'perms_lacking': [],
        'opts': opts,
        'objects_name': objects_name,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'media': modeladmin.media,
    }

    request.current_app = modeladmin.admin_site.name
    return TemplateResponse(
        request, "admin/admin_actions/get_csv_confirmation.html", context)


get_csv.short_description = _('Get selected %(verbose_name_plural)s CSV')
get_csv.allowed_permissions = ['view']
