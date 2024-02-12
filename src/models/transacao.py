from pydantic import BaseModel


class TransacaoModel(BaseModel):
    id: int | None = None
    cliente_id: int | None = None
    valor: int
    tipo: str
    descricao: str
    realizada_em: str | None = None

    def __str__(self):
        return f"{self.id} | {self.cliente_id} | {self.valor} | {self.tipo} | {self.descricao} | {self.realizada_em}"