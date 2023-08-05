# -*- coding: utf-8 -*-

import hmac
import json
import hashlib
import requests
from decimal import Decimal
from .error import APIError


class FixedFloatAPI:
    FIXED = 'fixed'
    FLOAT = 'float'

    STEP_PENDING  = 'pending'
    STEP_EXCHANGE = 'exchange'
    STEP_EXPIRED  = 'expired'
    STEP_DONE     = 'done'
    STEP_REJECTED = 'rejected'

    STATUS_NEW       = 0
    STATUS_PENDING   = 1
    STATUS_EXCHANGE  = 2
    STATUS_WITHDRAW  = 3
    STATUS_DONE      = 4
    STATUS_EXPIRED   = 5
    STATUS_REJECTED  = 6
    STATUS_EMERGENCY = 7
    STATUS_REFUND    = 8

    URL = 'https://fixedfloat.com/api'


    def __init__(self, key=None, secret=None):
        self.key    = key
        self.secret = secret

    def sign(self, params):
        if isinstance(params, dict):
            parts = []
            for k in params:
                parts.append('%s=%s' % (k, params[k]))
            payload = '&'.join(parts)
        else:
            payload = params
        return hmac.new(
            key=self.secret.encode(),
            msg=payload.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()


    def request(self, method, params={}, **kwargs):
        url = self.URL + method
        headers = {
            'X-API-KEY':  self.key,
            'X-API-SIGN': self.sign(params)
        }
        r = requests.post(url, data=params, headers=headers, **kwargs)
        result = json.loads(r.text, parse_float=Decimal)
        if result['code'] == 0:
            return result['data']
        else:
            raise APIError(result['code'], result['msg'])

    # Public
    def getCurrencies(self, params={}, **kwargs):
        return self.request('/v1/getCurrencies', params, **kwargs)

    def getPair(self, params={}, **kwargs):
        return self.request('/v1/getPair', params, **kwargs)

    def getPrice(self, params={}, **kwargs):
        return self.request('/v1/getPrice', params, **kwargs)

    # Orders
    def createOrder(self, params={}, **kwargs):
        return self.request('/v1/createOrder', params, **kwargs)

    def getOrder(self, params={}, **kwargs):
        return self.request('/v1/getOrder', params, **kwargs)

    def setEmergency(self, params={}, **kwargs):
        return self.request('/v1/setEmergency', params, **kwargs)
