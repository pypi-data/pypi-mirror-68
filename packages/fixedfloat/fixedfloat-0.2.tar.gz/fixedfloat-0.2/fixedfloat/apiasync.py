# -*- coding: utf-8 -*-

import json
import aiohttp
from decimal import Decimal
from .api import FixedFloatAPI
from .error import APIError


class FixedFloatAPIAsync(FixedFloatAPI):
    async def request(self, method, params={}, **kwargs):
        url = self.URL + method
        headers = {
            'X-API-KEY':  self.key,
            'X-API-SIGN': self.sign(params)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params, headers=headers, **kwargs) as response:
                text = await response.text()
                result = json.loads(text, parse_float=Decimal)
                if result['code'] == 0:
                    return result['data']
                else:
                    raise APIError(result['code'], result['msg'])

    # Public
    async def getCurrencies(self, params={}, **kwargs):
        return await self.request('/v1/getCurrencies', params, **kwargs)

    async def getPair(self, params={}, **kwargs):
        return await self.request('/v1/getPair', params, **kwargs)

    async def getPrice(self, params={}, **kwargs):
        return await self.request('/v1/getPrice', params, **kwargs)

    # Orders
    async def createOrder(self, params={}, **kwargs):
        return await self.request('/v1/createOrder', params, **kwargs)

    async def getOrder(self, params={}, **kwargs):
        return await self.request('/v1/getOrder', params, **kwargs)

    async def setEmergency(self, params={}, **kwargs):
        return await self.request('/v1/setEmergency', params, **kwargs)
