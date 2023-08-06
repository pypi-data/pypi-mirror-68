# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas.fields import GenFunction, PersistentIdentifier
from invenio_rest.serializer import BaseSchema as Schema
# noinspection PyUnusedLocal
from marshmallow import fields, missing, pre_load


def schema_from_context(_, context):
    """Get the record's schema from context."""
    record = (context or {}).get('record', {})
    return record.get("_schema", missing)


def bucket_from_context(_, context):
    """Get the record's bucket from context."""
    record = (context or {}).get('record', {})
    return record.get('_bucket', missing)


def files_from_context(_, context):
    """Get the record's files from context."""
    record = (context or {}).get('record', {})
    return record.get('_files', missing)


def get_id(obj, context):
    """Get record id."""
    pid = context.get('pid')
    return pid.pid_value if pid else missing


class InvenioRecordMetadataSchemaV1Mixin(Schema):
    _schema = GenFunction(
        attribute="$schema",
        data_key="$schema",
        deserialize=schema_from_context,  # to be added only when loading
    )
    id = PersistentIdentifier()

    @pre_load
    def handle_load(self, instance, **kwargs):
        instance.pop('_files', None)

        #
        # modified handling id from default invenio way:
        #
        # we need to use the stored id in dump (in case the object
        # is referenced, the id should be the stored one, not the context one)
        #
        # for data loading, we need to overwrite the id by the context - to be sure no one
        # is trying to overwrite the id
        #
        id_ = get_id(instance, self.context)
        if id_ is not missing:
            instance['id'] = str(id_)
        else:
            instance.pop('id', None)
        return instance


class InvenioRecordSchemaV1Mixin(Schema):
    """Invenio record"""

    id = PersistentIdentifier()
    metadata = fields.Nested(InvenioRecordMetadataSchemaV1Mixin, required=False)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    files = GenFunction(
        serialize=files_from_context, deserialize=files_from_context)
