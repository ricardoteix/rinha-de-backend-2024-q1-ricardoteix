from pydantic import BaseModel

from transacao import TransacaoModel
from saldo import SaldoModel


class ExtratoModel(BaseModel):
    saldo: SaldoModel
    ultimas_transacoes: list[TransacaoModel] = []
