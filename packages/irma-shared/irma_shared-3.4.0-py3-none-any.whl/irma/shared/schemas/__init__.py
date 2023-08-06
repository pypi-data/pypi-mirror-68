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

from marshmallow import ValidationError

from .artifact import ArtifactSchema
from .file import FileSchemaV2, FileSchemaV3
from .tag import TagSchema


__all__ = (
    'apiid',
    'ArtifactSchema',
    'FileSchemaV2',
    'FileSchemaV3',
    'TagSchema',
    'ValidationError',
)


from .artifact import Artifact
from .file import File
from .fileext import FileExt
from .probe import Probe
from .scan import Scan
from .srcode import ScanRetrievalCode
from .tag import Tag
from .user import User


def apiid(obj):  # pragma: no cover
    if isinstance(
            obj, (Artifact, File, FileExt, Probe, Scan, ScanRetrievalCode,
                  Tag, User)):
        return obj.id
    else:
        return obj
