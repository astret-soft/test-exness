import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from hypothesis import given
from hypothesis import strategies as st
from jsonschema import validate

from constants import *
from main import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_version():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('app/version')
    assert response.status_code == 200
    validate(
        response.json(),
        {
            'type': 'object',
            'properties': {
                'version': {
                    'type': 'number',
                }
            },
            'additionalProperties': False,
            'required': [
                'version'
            ]
        }
    )


@pytest.mark.asyncio
async def test_get_us_code_all():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('us-code', params={'code': None})
    assert response.status_code == 200, response.content
    result = {item['us_code']: item['us_tax'] for item in response.json()}
    assert result == {item.value: item.tax for item in USCodeEnum}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'us_code', list(USCodeEnum)
)
async def test_get_us_code(us_code: USCodeEnum):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/us-code', params={
            'code': us_code.value
        })
    assert response.status_code == 200, response.content
    assert response.json() == [{
        'us_code': us_code.value,
        'us_tax': us_code.tax
    }]


@pytest.mark.asyncio
@given(
    total_cost_to_discount=st.sampled_from(TOTAL_COST_TO_DISCOUNT),
    us_code=st.sampled_from(USCodeEnum),
)
async def test_total_price(total_cost_to_discount, us_code):
    price, discount = total_cost_to_discount
    async with AsyncClient(app=app, base_url='http://test') as ac:
        data = {
            'qty': 1,
            'price': price,
            'us_code': us_code.value
        }
        response = await ac.post('/total-price', json=data)
        assert response.status_code == 200, response.content
        actual = response.json()
        validate(
            actual,
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
        expected = {
            'discount_for_total_price': discount,
            'us_tax': us_code.tax,
            'total_price': price * discount / 100 * (100 - us_code.tax) / 100
        }
        assert actual == expected, data
