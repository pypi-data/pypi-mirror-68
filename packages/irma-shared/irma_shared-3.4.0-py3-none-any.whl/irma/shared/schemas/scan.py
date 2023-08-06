#
# Copyright (c) 2013-2019 Quarkslab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

from marshmallow import fields, Schema, post_load
from marshmallow_enum import EnumField

from ..csts import ScanPriority, ScanStatus
from .helpers import timestamp_to_date


class ScanSchemaV3(Schema):
    id = fields.UUID(attribute="external_id")
    date = fields.Number()
    status = fields.Integer(allow_none=True)

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    infected = fields.Integer()
    total = fields.Integer()

    force = fields.Boolean()
    resubmit_files = fields.Boolean()
    mimetype_filtering = fields.Boolean()
    priority = EnumField(ScanPriority)

    @post_load
    def make_object(self, data, **kwargs):
        return Scan(**data)


class ScanSchemaV2(Schema):
    id = fields.UUID(attribute="external_id")
    date = fields.Number()
    status = fields.Integer(allow_none=True)

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    force = fields.Boolean()
    resubmit_files = fields.Boolean()
    mimetype_filtering = fields.Boolean()

    results = fields.Nested(
        'FileExtSchemaV2',
        many=True,
        attribute="files_ext",
        exclude=('probe_results', 'file_infos', 'other_results')
    )

    @post_load
    def make_object(self, data, **kwargs):
        return Scan(**data)


class Scan:

    def __init__(
            self, external_id, *, date=None, status=None,
            probes_finished=None, probes_total=None,
            infected=None, total=None,
            force=None, resubmit_files=None, mimetype_filtering=None,
            files_ext=None, priority=None):
        self.external_id = str(external_id)
        self.date = date
        self.status = ScanStatus(status) if status is not None else None

        self.probes_finished = probes_finished
        self.probes_total = probes_total

        if infected is not None or total is not None:
            # NOTE: trick that creates those fields only in v3
            self.infected = infected
            self.total = total

        self.force = force
        self.resubmit_files = resubmit_files
        self.mimetype_filtering = mimetype_filtering

        self.files_ext = files_ext
        self.priority = None if priority is None else \
            priority if isinstance(priority, ScanPriority) else \
            ScanPriority[priority]

    def is_launched(self):
        return self.status == ScanStatus.launched

    def is_finished(self):
        return self.status == ScanStatus.finished

    @property
    def pstatus(self):
        return self.status.name

    @property
    def pdate(self):
        return timestamp_to_date(self.date)

    @property
    def id(self):
        return self.external_id

    def __repr__(self):
        return "Scan." + self.id

    def __str__(self):
        ret = "Scan{"
        ret += "id: {}; ".format(self.id)
        ret += "date: {}; ".format(self.pdate)
        ret += "status: {}; ".format(self.pstatus)
        if self.probes_total:
            ret += "probes progress: {}/{}; ".format(
                    self.probes_finished, self.probes_total)
        if hasattr(self, 'total'):
            ret += "infected: {}/{}; ".format(self.infected, self.total)
        if self.files_ext is not None:
            ret += "files_ext: {}; ".format(self.files_ext)

        options = []
        if self.force:
            options.append("force")
        if self.mimetype_filtering:
            options.append("mime_filter")
        if self.resubmit_files:
            options.append("resubmit")
        if self.priority is not None:
            options.append("priority:{}".format(self.priority.name))
        if options:
            ret += "options: [" + ",".join(options) + "]; "
        ret += "}"
        return ret

    def __eq__(self, other):
        return isinstance(other, Scan) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)
