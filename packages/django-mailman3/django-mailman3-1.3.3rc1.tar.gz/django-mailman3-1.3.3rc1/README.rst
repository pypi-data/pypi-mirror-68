==============================
Django library for Mailman UIs
==============================

This package contains libraries and templates for Django-based interfaces
interacting with Mailman.

To use this application, add ``django_mailman3`` to the ``INSTALLED_APPS`` list
in your Django server's settings file.


NEWS
====

1.3.3rc1 (2020-05-09)
---------------------

- Hide "Account Connections" tab in accounts if no social account providers are
  installed. (See !54)
- Use bold font for form labels (See !82)
- Update a user's preferred_address in Mailman Core when a user updates their
  primary address in Profile. (Closes #32)

License
=======

Django-mailman is licensed under the
`GPL v3.0 <http://www.gnu.org/licenses/gpl-3.0.html>`_

Copyright (C) 2017-2019 by the Free Software Foundation, Inc.
