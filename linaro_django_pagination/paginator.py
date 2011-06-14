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


from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage


class InfinitePaginator(Paginator):
    """
    Paginator designed for cases when it's not important to know how many total
    pages.  This is useful for any object_list that has no count() method or
    can be used to improve performance for MySQL by removing counts.

    The orphans parameter has been removed for simplicity and there's a link
    template string for creating the links to the next and previous pages.
    """

    def __init__(self, object_list, per_page, allow_empty_first_page=True,
        link_template='/page/%d/'):
        orphans = 0  # no orphans
        super(InfinitePaginator, self).__init__(object_list, per_page, orphans,
            allow_empty_first_page)
        # no count or num pages
        del self._num_pages, self._count
        # bonus links
        self.link_template = link_template

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        page_items = self.object_list[bottom:top]
        # check moved from validate_number
        if not page_items:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return InfinitePage(page_items, number, self)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        raise NotImplementedError
    count = property(_get_count)

    def _get_num_pages(self):
        """
        Returns the total number of pages.
        """
        raise NotImplementedError
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        raise NotImplementedError
    page_range = property(_get_page_range)


class InfinitePage(Page):

    def __repr__(self):
        return '<Page %s>' % self.number

    def has_next(self):
        """
        Checks for one more item than last on this page.
        """
        try:
            self.paginator.object_list[self.number * self.paginator.per_page]
        except IndexError:
            return False
        return True

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        return ((self.number - 1) * self.paginator.per_page +
            len(self.object_list))

    #Bonus methods for creating links

    def next_link(self):
        if self.has_next():
            return self.paginator.link_template % (self.number + 1)
        return None

    def previous_link(self):
        if self.has_previous():
            return self.paginator.link_template % (self.number - 1)
        return None


class FinitePaginator(InfinitePaginator):
    """
    Paginator for cases when the list of items is already finite.

    A good example is a list generated from an API call. This is a subclass
    of InfinitePaginator because we have no idea how many items exist in the
    full collection.

    To accurately determine if the next page exists, a FinitePaginator MUST be
    created with an object_list_plus that may contain more items than the
    per_page count.  Typically, you'll have an object_list_plus with one extra
    item (if there's a next page).  You'll also need to supply the offset from
    the full collection in order to get the page start_index.

    This is a very silly class but useful if you love the Django pagination
    conventions.
    """

    def __init__(self, object_list_plus, per_page, offset=None,
        allow_empty_first_page=True, link_template='/page/%d/'):
        super(FinitePaginator, self).__init__(object_list_plus, per_page,
            allow_empty_first_page, link_template)
        self.offset = offset

    def validate_number(self, number):
        super(FinitePaginator, self).validate_number(number)
        # check for an empty list to see if the page exists
        if not self.object_list:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        # remove the extra item(s) when creating the page
        page_items = self.object_list[:self.per_page]
        return FinitePage(page_items, number, self)


class FinitePage(InfinitePage):

    def has_next(self):
        """
        Checks for one more item than last on this page.
        """
        try:
            self.paginator.object_list[self.paginator.per_page]
        except IndexError:
            return False
        return True

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        ## TODO should this holler if you haven't defined the offset?
        return self.paginator.offset
