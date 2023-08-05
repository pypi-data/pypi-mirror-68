==============
FixedFloat API
==============

This is the official Python wrapper for the `FixedFloat API <https://fixedfloat.com/api>`_.

Quick Start
-----------

`Generate an API Key <https://fixedfloat.com/apikey>`_.

.. code:: bash

    pip install fixedfloat

Synchronous method calls

.. code:: python

    from fixedfloat import FixedFloatAPI
    
    ff = FixedFloatAPI(
        key=apiKey,
        secret=apiSecret
    )

    # Get a list of all currencies
    currencies = ff.getCurrencies()

    # Get pair info
    fr, to = 'LTC', 'ETH'
    amount = '0.1'
    pair = ff.getPair({'from': fr, 'to': to})

    # Get price
    # price = ff.getPrice({'fromCurrency': fr, 'toCurrency': to, 'fromQty': amount, 'type': 'fixed'})

    # Create order
    address = '1NdCTQ1ufXCZp6CHhDJGNvHpGztoYxWWhb'
    order = ff.createOrder({
        'fromCurrency': fr,
        'toCurrency': to,
        'toQty': amount,
        'toAddress': address,
        'type': 'fixed'
    })

    # Get order info
    orderID = '5VSKHM'
    token = 'YQR2XrznWkuVHsAiBSQeAnI4t0EQGj1HElYFlF2O'
    order = ff.getOrder({'id': orderID, 'token': token})

Asynchronous method calls

.. code:: python

    from fixedfloat import FixedFloatAPIAsync
    
    ff = FixedFloatAPIAsync(
        key=apiKey,
        secret=apiSecret
    )

    loop = asyncio.get_event_loop()

    # Get a list of all currencies
    currencies = loop.run_until_complete(ff.getCurrencies())

    # Get pair info
    fr, to = 'LTC', 'ETH'
    amount = '0.1'
    pair = loop.run_until_complete(ff.getPair({'from': fr, 'to': to}))

    # Get price
    # price = loop.run_until_complete(ff.getPrice({'fromCurrency': fr, 'toCurrency': to, 'fromQty': amount, 'type': 'fixed'}))

    # Create order
    address = '1NdCTQ1ufXCZp6CHhDJGNvHpGztoYxWWhb'
    order = loop.run_until_complete(ff.createOrder({
        'fromCurrency': fr,
        'toCurrency': to,
        'toQty': amount,
        'toAddress': address,
        'type': 'fixed'
    }))

    # Get order info
    orderID = '5VSKHM'
    token = 'YQR2XrznWkuVHsAiBSQeAnI4t0EQGj1HElYFlF2O'
    order = loop.run_until_complete(ff.getOrder({'id': orderID, 'token': token}))
