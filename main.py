import uvicorn
from typing import Optional

from fastapi import FastAPI

from constants import *
from models import *

app = FastAPI()


@app.post('/total-price', response_model=TotalPriceResponse)
async def total_price(request: TotalPriceRequest):
    return {
        'discount_for_total_price': request.discount_for_total_price,
        'us_tax': request.us_tax,
        'total_price': request.total_price
    }


@app.get('/us-code', response_model=USCodeResponse)
async def total_price(code: Optional[USCodeEnum]):
    return [
        {**zip(('us_code', 'us_tax'), value)}
        for value in filter(
            lambda us_code:
            code is None or code == us_code,
            USCodeEnum
        )
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4242)
