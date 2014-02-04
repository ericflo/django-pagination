Version History
***************

.. _version_2_0:

Version 2.0
===========


* Revived the project as a fork of
  git://github.com/ericflo/django-pagination.git. The project now has a new
  maintainer (Zygmunt Krynicki) and a new home (on pypi and launchpad).

* Merged a lot of branches of the old project. In general this was made to show
  people "here is the new good stuff" and to get as much contributions, back
  into the trunk, as possible.

* Merge a lot of translations: de, es, fr, it, nn, no, pl, pt, pt_BR, ru and
  tr. Translations are still in a bad state (they are not built automatically,
  they are in incorrect place) but the first step is done.

* Add support for custom pagination templates. You can now use the optional
  argument on paginate to use different template::

    {% autopaginate obj_list %}
    ...
    {% paginate using "something/custom_template.html" %}

* Pagination template has support for specific blocks. Those blocks are
  'previouslink', 'pagelinks' and 'nextlink'.  Make sure to base your template
  on pagination/pagination.html end extend the blocks you care about.

* Add support for using multiple paginations on a single page. Simply use
  multiple autopaginate/paginate tags. The only limitation is that you must use
  paginate before using the next autopaginate tag. For an example see the test
  project and the example application inside.

* Simplify building documentation. To build the documentation simply run
  `setup.py build_sphinx`. You will need sphinx installed obviously.

* Simplify running tests. To run tests just invoke `setup.py test`. That's all!
  This is based on the goodness of django-testproject that simplifies setting
  up helper projects just for testing.


Version 1.0.7
=============

* Last release from previous upstream developer.
