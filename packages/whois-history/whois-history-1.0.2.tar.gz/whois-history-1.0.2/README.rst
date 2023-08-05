========
Overview
========

The client library for
`Whois History API <https://whois-history.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============
::

    pip install whois-history

Examples
========

Full API documentation available `here <https://whois-history.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

::

    from whoishistory import ApiClient

    client = ApiClient('Your API key')

Make basic requests
-------------------

::

    # Check how many records available. It doesn't deduct credits.
    print(client.preview('whoisxmlapi.com'))

    # Get actual list of records.
    print(client.purchase('whoisxmlapi.com'))


Additional options
-------------------
You can specify search options for these methods.


::

    import datetime

    d = datetime.date(2017, 1, 1)

    print(client.preview('whoisxmlapi.com'),
          sinceDate=d,
          createdDateFrom=d,
          createdDateTo=d,
          updatedDateFrom=d,
          updatedDateTo=d,
          expiredDateFrom=d,
          expiredDateTo=d,
    )

