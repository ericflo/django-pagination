# Copyright (c) 2008, Eric Florenzano
# Copyright (c) 2010, 2011 Linaro Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of the author nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from django.conf import settings


DEFAULT_PAGINATION = getattr(
    settings, 'PAGINATION_DEFAULT_PAGINATION', 20)
DEFAULT_WINDOW = getattr(
    settings, 'PAGINATION_DEFAULT_WINDOW', 4)
DEFAULT_MARGIN = getattr(
    settings, 'PAGINATION_DEFAULT_MARGIN', DEFAULT_WINDOW)
DEFAULT_ORPHANS = getattr(
    settings, 'PAGINATION_DEFAULT_ORPHANS', 0)
INVALID_PAGE_RAISES_404 = getattr(
    settings, 'PAGINATION_INVALID_PAGE_RAISES_404', False)
DISPLAY_PAGE_LINKS = getattr(
    settings, 'PAGINATION_DISPLAY_PAGE_LINKS', True)
PREVIOUS_LINK_DECORATOR = getattr(
    settings, 'PAGINATION_PREVIOUS_LINK_DECORATOR', "&lsaquo;&lsaquo; ")
NEXT_LINK_DECORATOR = getattr(
    settings, 'PAGINATION_NEXT_LINK_DECORATOR', " &rsaquo;&rsaquo;")
DISPLAY_DISABLED_PREVIOUS_LINK = getattr(
    settings, 'PAGINATION_DISPLAY_DISABLED_PREVIOUS_LINK', False)
DISPLAY_DISABLED_NEXT_LINK = getattr(
    settings, 'PAGINATION_DISPLAY_DISABLED_NEXT_LINK', False)
DISABLE_LINK_FOR_FIRST_PAGE = getattr(
    settings, 'PAGINATION_DISABLE_LINK_FOR_FIRST_PAGE', True)
