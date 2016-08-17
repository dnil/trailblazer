# -*- coding: utf-8 -*-
from datetime import datetime
import json

import alchy
from sqlalchemy import Column, types, UniqueConstraint


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError('Type not serializable')


class JsonModel(alchy.ModelBase):

    def to_json(self, pretty=False):
        """Serialize Model to JSON."""
        kwargs = dict(indent=4, sort_keys=True) if pretty else dict()
        return json.dumps(self.to_dict(), default=json_serial, **kwargs)


Model = alchy.make_declarative_base(Base=JsonModel)


class Analysis(Model):

    """Analysis record."""

    __table_args__ = (UniqueConstraint('case_id', 'started_at', 'status',
                                       name='_uc_case_start_status_step'),)

    id = Column(types.Integer, primary_key=True)
    case_id = Column(types.String(128))

    # metadata
    pipeline = Column(types.Enum('mip'))
    pipeline_version = Column(types.String(32))
    started_at = Column(types.DateTime)
    completed_at = Column(types.DateTime)
    runtime = Column(types.Integer)
    cputime = Column(types.Integer)
    status = Column(types.Enum('running', 'completed', 'failed'))
    root_dir = Column(types.Text)
    config_path = Column(types.Text)
    type = Column(types.Enum('exomes', 'genomes'))
    failed_step = Column(types.String(128))
    failed_at = Column(types.DateTime)
    comment = Column(types.Text)
    is_deleted = Column(types.Boolean, default=False)
    _samples = Column(types.Text)

    @property
    def samples(self):
        return self._samples.split(',') if self._samples else []

    @samples.setter
    def samples(self, sample_list):
        """Serialize a list of sample ids."""
        self._samples = ','.join(sample_list)
