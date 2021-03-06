# -*- coding: utf-8 -*-
import datetime as dt
from pathlib import Path
import logging
from typing import List

log = logging.getLogger(__name__)


class FastqHandler:

    @staticmethod
    def name_file(lane: int, flowcell: str, sample: str, read: int,
                  undetermined: bool=False, date: dt.datetime=None, index: str=None) -> str:
        """Name a FASTQ file following MIP conventions."""
        flowcell = f"{flowcell}-undetermined" if undetermined else flowcell
        date_str = date.strftime('%y%m%d') if date else '171015'
        index = index if index else 'XXXXXX'
        return f"{lane}_{date_str}_{flowcell}_{sample}_{index}_{read}.fastq.gz"

    def link(self, family: str, sample: str, analysis_type: str, files: List[str]):
        """Link FASTQ files for a sample."""
        root_dir = Path(self.families_dir) / family / analysis_type / sample / 'fastq'
        root_dir.mkdir(parents=True, exist_ok=True)
        for fastq_data in files:
            fastq_path = Path(fastq_data['path'])
            fastq_name = self.name_file(
                lane=fastq_data['lane'],
                flowcell=fastq_data['flowcell'],
                sample=sample,
                read=fastq_data['read'],
                undetermined=fastq_data['undetermined'],
            )
            dest_path = root_dir / fastq_name
            if not dest_path.exists():
                log.info(f"linking: {fastq_path} -> {dest_path}")
                dest_path.symlink_to(fastq_path)
            else:
                log.debug(f"destination path already exists: {dest_path}")
