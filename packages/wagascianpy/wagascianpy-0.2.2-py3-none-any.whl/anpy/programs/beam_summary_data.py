#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc

import anpy.program
import anpy.program_builder

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class BeamSummaryDataBuilder(anpy.program_builder.ProgramBuilder, ABC):
    """
    Add Beam Summary Data (BSD) info to the run
    """

    def __init__(self,
                 bsd_database_location,
                 bsd_repository_location,
                 download_bsd_database_location="/tmp/bsd/bsddb.db",
                 download_bsd_repository_location="/tmp/bsd",
                 t2krun=10,
                 recursive=True):
        super(BeamSummaryDataBuilder, self).__init__()
        self._program = anpy.program.Program()
        self._add_beam_summary_data(
            bsd_database_location=bsd_database_location,
            bsd_repository_location=bsd_repository_location,
            download_bsd_database_location=download_bsd_database_location,
            download_bsd_repository_location=download_bsd_repository_location,
            t2krun=t2krun,
            recursive=recursive)

    def reset(self):
        self._program = anpy.program.Program()

    @property
    def program(self):
        my_program = self._program
        self.reset()
        return my_program
