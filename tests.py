import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from hypothesis import given
from hypothesis import strategies as st
from jsonschema import validate

from constants import *

MACHINE_DIFF = 0.001

app = FastAPI()


client = TestClient(app)


@pytest.mark.asyncio
async def test_read_us_code_all():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/us-code',)
    assert response.status_code == 200
    assert response.json() == [{
        'us_code': value[0],
        'us_tax': value[1]
    } for value in USCodeEnum]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    list(USCodeEnum)
)
async def test_read_us_code(us_code: USCodeEnum):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/us-code', params={
            'code': us_code[0]
        })
    assert response.status_code == 200
    assert response.json() == [{
        'us_code': us_code[0],
        'us_tax': us_code[1]
    }]


@pytest.mark.asyncio
@given(
    qty=st.integers(min_value=0),
    price=st.integers(min_value=0),
    us_code=st.sampled_from(list(map(
        lambda value: value[0] , USCodeEnum
    ))),
)
async def test_total_price(qty, price, us_code):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.post('/total-price', {
            'qty': qty,
            'price': price,
            'us_code': us_code
        })
    assert response.status_code == 200
    validate(
        response.json(),
        {
            'type': 'object',
            'properties': {
                'discount_for_total_price': {
                    'type': 'number',
                    'minimum': 0,
                },
                'us_tax': {
                    'type': 'number',
                    'minimum': 0,
                },
                'total_price': {
                    'type': 'number',
                    'minimum': 0,
                }
            },
            'additionalProperties': False,
            'required': [
                  'discount_for_total_price',
                  'us_tax',
                  'total_price'
            ]
        }
    )


@pytest.mark.asyncio
@given(
    total_cost_to_discount=TOTAL_COST_TO_DISCOUNT
)
async def test_total_price_limits(total_cost_to_discount):
    edge, discount = total_cost_to_discount
    for price, status_code in (
            (edge, 200),
            (edge - MACHINE_DIFF, 400),
            (edge + MACHINE_DIFF, 400),
    ):
        async with AsyncClient(app=app, base_url='http://test') as ac:
            us_code = st.sampled_from(list(map(
                lambda value: value[0] , USCodeEnum
            ))).example()
            response = await ac.post('/total-price', {
                'qty': 1,
                'price': 1,
                'us_code': us_code
            })
            assert response.status_code == status_code
            if 200 <= status_code < 300:
                continue
            assert response.json() == [{
                'discount_for_total_price': USCodeEnum[us_code].value[0],
                'us_tax': us_code[1],
                'total_price': discount
            }]
