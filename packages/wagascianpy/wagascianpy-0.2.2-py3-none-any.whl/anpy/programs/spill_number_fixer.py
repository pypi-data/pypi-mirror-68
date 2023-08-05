#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc

import anpy.program
import anpy.program_builder

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class SpillNumberFixerBuilder(anpy.program_builder.ProgramBuilder, ABC):
    """ Fix spill number """

    def __init__(self):
        super(SpillNumberFixerBuilder, self).__init__()
        self._program = anpy.program.Program()
        self._add_spill_number_fixer(enable_graphics=False)

    def reset(self):
        self._program = anpy.program.Program()

    @property
    def program(self):
        my_program = self._program
        self.reset()
        return my_program
