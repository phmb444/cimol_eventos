CREATE TABLE "usuarios"(
    "id" BIGINT NOT NULL,
    "nome" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "senha" VARCHAR(255) NOT NULL,
    "telefone" VARCHAR(255) NOT NULL,
    "tipo_usuario" VARCHAR(255) CHECK
        (
            "tipo_usuario" IN(
                'organizador',
                'palestrante',
                'interno',
                'externo',
                'professor'
            )
        ) NOT NULL,
        "cadastro" DATE NOT NULL
);
ALTER TABLE
    "usuarios" ADD PRIMARY KEY("id");
ALTER TABLE
    "usuarios" ADD CONSTRAINT "usuarios_email_unique" UNIQUE("email");
ALTER TABLE
    "usuarios" ADD CONSTRAINT "usuarios_telefone_unique" UNIQUE("telefone");
CREATE TABLE "eventos"(
    "id_evento" BIGINT NOT NULL,
    "nome_evento" VARCHAR(255) NOT NULL,
    "descricao" TEXT NOT NULL,
    "data_inicio" DATE NOT NULL,
    "tempo_inicio" TIME(0) WITHOUT TIME ZONE NOT NULL,
    "data_fim" DATE NOT NULL,
    "tempo_fim" TIME(0) WITHOUT TIME ZONE NOT NULL,
    "local" VARCHAR(255) NOT NULL,
    "vagas" INTEGER NOT NULL,
    "aberto" BOOLEAN NOT NULL DEFAULT '0',
    "data_cadastro" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "organizador" BIGINT NOT NULL,
    "id_icon" BIGINT NOT NULL,
    "id_banner" BIGINT NOT NULL
);
ALTER TABLE
    "eventos" ADD PRIMARY KEY("id_evento");
CREATE TABLE "palestrante"(
    "id_palestrante" BIGINT NOT NULL,
    "id_usuario" BIGINT NOT NULL,
    "id_evento" BIGINT NOT NULL,
    "perfil" TEXT NOT NULL,
    "tema_apresentacao" VARCHAR(255) NOT NULL,
    "id_foto" BIGINT NOT NULL
);
ALTER TABLE
    "palestrante" ADD PRIMARY KEY("id_palestrante");
CREATE TABLE "incricoes"(
    "id_inscricao" BIGINT NOT NULL,
    "id_evento" BIGINT NOT NULL,
    "id_usuario" BIGINT NOT NULL,
    "data_inscricao" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "status" VARCHAR(255) CHECK
        (
            "status" IN('inscrito', 'cancelado')
        ) NOT NULL DEFAULT 'inscrito'
);
ALTER TABLE
    "incricoes" ADD PRIMARY KEY("id_inscricao");
CREATE TABLE "recuperacao_senha"(
    "id" BIGINT NOT NULL,
    "id_usuario" BIGINT NOT NULL,
    "codigo_verificacao" VARCHAR(255) NOT NULL,
    "data_solicitacao" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "data_validacao" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "status" VARCHAR(255) CHECK
        (
            "status" IN('pendente', 'concluido')
        ) NOT NULL DEFAULT 'pendente'
);
ALTER TABLE
    "recuperacao_senha" ADD PRIMARY KEY("id");
CREATE TABLE "foto"(
    "id_foto" BIGINT NOT NULL,
    "file_name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "foto" ADD PRIMARY KEY("id_foto");
ALTER TABLE
    "eventos" ADD CONSTRAINT "eventos_organizador_foreign" FOREIGN KEY("organizador") REFERENCES "usuarios"("id");
ALTER TABLE
    "incricoes" ADD CONSTRAINT "incricoes_id_usuario_foreign" FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id");
ALTER TABLE
    "palestrante" ADD CONSTRAINT "palestrante_id_usuario_foreign" FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id");
ALTER TABLE
    "incricoes" ADD CONSTRAINT "incricoes_id_evento_foreign" FOREIGN KEY("id_evento") REFERENCES "eventos"("id_evento");
ALTER TABLE
    "eventos" ADD CONSTRAINT "eventos_id_icon_foreign" FOREIGN KEY("id_icon") REFERENCES "foto"("id_foto");
ALTER TABLE
    "palestrante" ADD CONSTRAINT "palestrante_id_evento_foreign" FOREIGN KEY("id_evento") REFERENCES "eventos"("id_evento");
ALTER TABLE
    "recuperacao_senha" ADD CONSTRAINT "recuperacao_senha_id_usuario_foreign" FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id");
ALTER TABLE
    "eventos" ADD CONSTRAINT "eventos_id_banner_foreign" FOREIGN KEY("id_banner") REFERENCES "foto"("id_foto");
ALTER TABLE
    "palestrante" ADD CONSTRAINT "palestrante_id_foto_foreign" FOREIGN KEY("id_foto") REFERENCES "foto"("id_foto");