# -*- coding: utf-8 -*-

# Copyright (c) 2013, Theo Crevon
# Copyright (c) 2013, Greg Leclercq
#
# See the file LICENSE for copying permission.

REGISTERED = 'REGISTERED'
DEPRECATED = 'DEPRECATED'

MAX_REASON_LENGTH = 256
MAX_DETAILS_LENGTH = 32768
MAX_INPUT_LENGTH = 32000
MAX_RESULT_LENGTH = 32000

# A SWF workflow cannot last more than a year, and workflows informations are
# accessible for maximum 90 days (retention set at domain creation).
# Hence this value is an upper limit to retrieve *all* open/closed workflow
# executions on a given region+domain.
MAX_WORKFLOW_AGE = 366 + 90 + 1
