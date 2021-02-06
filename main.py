import uvicorn
from typing import Optional

from fastapi import FastAPI

from constants import *
from models import *

app = FastAPI()


@app.get('/app/version')
async def version():
    return {'version': 1}


@app.post('/total-price', response_model=TotalPriceResponse)
async def total_price(request: TotalPriceRequest):
    return {
        'discount_for_total_price': request.discount_for_total_price,
        'us_tax': request.us_tax,
        'total_price': float(request.total_price)
    }


@app.get('/us-code', response_model=USCodeResponse)
async def us_code(code: Optional[str]):
    # note: нужно для возможного UI, чтобы выбирать штат
    return [
        {
            'us_code': item.value,
            'us_tax': item.tax
        } for item in USCodeEnum
        if not code or code == item.value
    ]


if __name__ == "__main__":
    # note: в задании нет требования все поднимать в docker и тд,
    # конфигурацию не создаю (yaml, json, env...)
    uvicorn.run(app, host='0.0.0.0', port=4242)
