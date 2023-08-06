# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Miroslav Bauer, CESNET.
#
# oarepo-references is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module for tracking and updating references in Invenio records."""

from __future__ import absolute_import, print_function

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_records import Record
from invenio_records.models import Timestamp
from invenio_search import current_search_client

from oarepo_references.models import RecordReference
from oarepo_references.signals import after_reference_update
from oarepo_references.utils import get_reference_uuid, keys_in_dict


class RecordReferenceAPI(object):
    """Represent a record reference."""

    indexer_version_type = None

    @classmethod
    def get_records(cls, reference, exact=False):
        """Retrieve multiple records by reference.

        :param reference: Reference URI
        :returns: A list of :class:`oarepo_references.models.RecordReference`
                  instances containing the reference.
        """
        with db.session.no_autoflush:
            if exact:
                query = RecordReference.query \
                    .filter(RecordReference.reference == reference) \
                    .distinct(RecordReference.record_uuid)
            else:
                query = RecordReference.query \
                    .filter(RecordReference.reference.startswith(reference)) \
                    .distinct(RecordReference.record_uuid)

            return query.all()

    @classmethod
    def reindex_referencing_records(cls, ref, ref_obj=None):
        """
        Reindex all record that reference given ref.

        :param ref:         url to be checked
        :param ref_obj:     an object (record etc.) of the reference
        """
        refs = cls.get_records(ref)
        records = Record.get_records([r.record_uuid for r in refs])
        recids = [r.id for r in records]
        sender = ref_obj if ref_obj else ref
        indexed = after_reference_update.send(sender, references=recids, ref_obj=ref_obj)
        print('reference_update_reindex_handled', indexed)
        if not any([res[1] for res in indexed]):
            RecordIndexer().bulk_index(recids)
            RecordIndexer(version_type=cls.indexer_version_type).process_bulk_queue(
                es_bulk_kwargs={'raise_on_error': True})
            current_search_client.indices.flush()

    @classmethod
    def update_references_from_record(cls, record):
        """
        Gathers all references from a record and updates internal RecordReference table.

        :param record       invenio record
        """
        with db.session.begin_nested():
            # Find all entries for record id
            rrs = RecordReference.query.filter_by(record_uuid=record.model.id)
            rec_refs = list(set(list(keys_in_dict(record, required_types=(str,)))))
            db_refs = list(set([r[0] for r in rrs.values('reference')]))

            record.validate()

            # Delete removed/add added references
            for rr in rrs.all():
                if rr.reference not in rec_refs:
                    db.session.delete(rr)
            for ref in rec_refs:
                if ref not in db_refs:
                    ref_uuid = get_reference_uuid(ref)
                    rr = RecordReference(record_uuid=record.model.id, reference=ref,
                                         reference_uuid=ref_uuid)
                    db.session.add(rr)


__all__ = (
    'RecordReferenceAPI',
)
