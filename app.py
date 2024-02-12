from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from src.models.saldo import SaldoModel
from src.models.transacao import TransacaoModel

app = FastAPI()

API_PORT = os.getenv('API_PORT') or 80

conn = psycopg2.connect(dbname='rinha', user='rinha', password='rinha', cursor_factory=RealDictCursor)
@app.get("/clientes/{cliente_id}/extrato")
async def post_transacoes(cliente_id: int, transacao: TransacaoModel):
    global conn

    if conn is None or conn.closed:
        conn = psycopg2.connect(dbname='rinha', user='rinha', password='rinha', cursor_factory=RealDictCursor)

    pass

@app.post("/clientes/{cliente_id}/transacoes")
async def post_transacoes(cliente_id: int, transacao: TransacaoModel):
    global conn

    if conn is None or conn.closed:
        conn = psycopg2.connect(dbname='rinha', user='rinha', password='rinha', cursor_factory=RealDictCursor)

    cursor = conn.cursor()

    if len(transacao.descricao) < 1 or len(transacao.descricao) > 10:
        return JSONResponse(content={'message': 'descrição inválida'}, status_code=422, headers={})

    query_cliente = """select id, limite, saldo from clientes where id = %s;"""
    cursor.execute(query_cliente, (cliente_id,))
    result_cliente = cursor.fetchone()

    if result_cliente is None or len(result_cliente) == 0:
        return JSONResponse(content={'message': 'cliente não existe'}, status_code=404, headers={})

    if transacao.tipo not in ('c', 'd'):
        return JSONResponse(content={'message': 'operação inválida'}, status_code=422, headers={})

    op = 1
    if transacao.tipo == 'd':
        op = -1

    if result_cliente['saldo'] + (transacao.valor * op) < -result_cliente['limite']:
        return JSONResponse(content={'message': 'saldo inconsistente'}, status_code=422, headers={})

    query_transacao = """
        set session my.vars.cliente_id = %s;
        set session my.vars.valor = %s;

        insert into transacoes (cliente_id, valor, tipo, descricao) VALUES (
            current_setting('my.vars.cliente_id')::bigint, 
            current_setting('my.vars.valor')::bigint, %s, %s);
            
        update clientes set saldo = saldo + current_setting('my.vars.valor')::bigint 
            where id = current_setting('my.vars.cliente_id')::bigint and saldo + current_setting('my.vars.valor')::bigint < limite; 
            
        select id, limite, saldo from clientes where id = current_setting('my.vars.cliente_id')::bigint;
    """

    valor = transacao.valor * op
    cursor.execute(query_transacao, (cliente_id, valor, transacao.tipo, transacao.descricao))
    result_transacao = cursor.fetchone()

    conn.commit()
    cursor.close()



    code = 200
    headers = {
        'Content-Type': 'application/json'
    }
    content = {
        "limite": result_transacao['limite'],
        "saldo": result_transacao['saldo']
    }
    return JSONResponse(content=content, status_code=code, headers=headers)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    html_content = """
                <html>
                    <head>
                        <title>Some HTML in here</title>
                    </head>
                    <body style="background-color: #ffc300;text-align: center;">
                        <h1 style="font-family: monospace;">You Shall Not Pass!</h1>
                        <img src="https://img.elo7.com.br/product/685x685/2AC1DEC/placa-decorativa-quadro-filme-you-shall-not-pass-gv612-decoracao-sala.jpg">
                    </body>
                </html>
                """
    return HTMLResponse(content=html_content, status_code=404)


if __name__ == "__main__":
    uvicorn.run("app:app", port=int(API_PORT), log_level="info", host="0.0.0.0")
