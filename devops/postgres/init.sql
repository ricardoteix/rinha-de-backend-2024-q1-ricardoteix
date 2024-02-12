--CREATE DATABASE "rinha"
--    WITH
--    OWNER = postgres
--    ENCODING = 'UTF8'
--    CONNECTION LIMIT = -1
--    IS_TEMPLATE = False;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS clientes (
    id BIGSERIAL PRIMARY KEY,
    limite bigint NOT NULL,
    saldo bigint NOT NULL
);

INSERT INTO clientes (id, limite, saldo)
VALUES (1, 100000, 0), (2, 80000, 0), (3, 1000000, 0), (4, 10000000, 0), (5, 500000, 0);

ALTER SEQUENCE clientes_id_seq RESTART WITH 10;

--

CREATE TABLE IF NOT EXISTS transacoes (
    id BIGSERIAL PRIMARY KEY,
	cliente_id bigint REFERENCES clientes(id) NOT NULL,
    valor bigint NOT NULL,
    tipo VARCHAR(1) NOT NULL,
    descricao VARCHAR(10) NOT NULL,
    realizada_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

--CREATE TABLE IF NOT EXISTS pessoas (
--    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY, -- maybe use generating in backend simplifies and accelerate things
--    nome VARCHAR(100) COLLATE pg_catalog."default" NOT NULL,
--    apelido VARCHAR(32) COLLATE pg_catalog."default" NOT NULL,
--    nascimento DATE NOT NULL,
--    stack TEXT COLLATE pg_catalog."default"
--);
--
--ALTER TABLE pessoas ADD CONSTRAINT constraint_apelido UNIQUE (apelido);
--
--TRUNCATE TABLE pessoas;