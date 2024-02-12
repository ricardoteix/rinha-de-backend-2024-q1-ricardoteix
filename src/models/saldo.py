from pydantic import BaseModel
from datetime import datetime


class SaldoModel(BaseModel):
    total: int
    limite: int
    data_extrato: str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
