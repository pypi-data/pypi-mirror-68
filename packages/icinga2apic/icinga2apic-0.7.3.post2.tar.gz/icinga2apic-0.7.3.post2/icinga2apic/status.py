# -*- coding: utf-8 -*-
'''
Copyright 2017 fmnisme@gmail.com, Copyright 2020 christian@jonak.org

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Icinga 2 API status
'''

from __future__ import print_function
import logging

from icinga2apic.base import Base

LOG = logging.getLogger(__name__)


class Status(Base):
    '''
    Icinga 2 API status class
    '''

    base_url_path = 'v1/status'

    def list(self, component=None):
        '''
        retrieve status information and statistics for Icinga 2

        example 1:
        list()

        example 2:
        list('IcingaApplication')

        :param component: only list the status of this component
        :type component: string
        :returns: status information
        :rtype: dictionary
        '''

        url = self.base_url_path
        if component:
            url += "/{}".format(component)

        return self._request('GET', url)
