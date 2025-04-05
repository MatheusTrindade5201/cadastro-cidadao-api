"""add entities tables

Revision ID: 99eb71135e74
Revises: 3060fbce8cf3
Create Date: 2025-04-05 14:00:43.027632

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '99eb71135e74'
down_revision = '3060fbce8cf3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domicilio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cep', sa.String(length=10), nullable=False),
    sa.Column('municipio', sa.String(length=60), nullable=False),
    sa.Column('uf', sa.String(length=2), nullable=False),
    sa.Column('bairro', sa.String(length=60), nullable=False),
    sa.Column('tipo_logradouro', sa.String(length=20), nullable=False),
    sa.Column('nome_logradouro', sa.String(length=60), nullable=False),
    sa.Column('numero', sa.String(length=10), nullable=False),
    sa.Column('complemento', sa.String(length=20), nullable=True),
    sa.Column('pto_referencia', sa.String(length=60), nullable=True),
    sa.Column('microarea', sa.String(length=2), nullable=False),
    sa.Column('tipo_imovel', sa.String(length=2), nullable=False),
    sa.Column('telefone_residencia', sa.String(length=15), nullable=True),
    sa.Column('telefone_contato', sa.String(length=15), nullable=False),
    sa.Column('situacao_moradia', sa.String(length=20), nullable=False),
    sa.Column('localizacao', sa.String(length=60), nullable=False),
    sa.Column('tipo_domicilio', sa.String(length=60), nullable=False),
    sa.Column('material_predominante', sa.String(length=60), nullable=False),
    sa.Column('condicao_posse_producao_rural', sa.String(length=60), nullable=True),
    sa.Column('n_moradores', sa.Integer(), nullable=False),
    sa.Column('n_comodos', sa.Integer(), nullable=False),
    sa.Column('tipo_acesso', sa.String(length=60), nullable=False),
    sa.Column('energia_eletrica', sa.Boolean(), nullable=False),
    sa.Column('abastecimento_agua', sa.String(length=60), nullable=False),
    sa.Column('escoamento_banheiro', sa.String(length=60), nullable=False),
    sa.Column('agua_consumo', sa.String(length=60), nullable=False),
    sa.Column('destino_lixo', sa.String(length=60), nullable=False),
    sa.Column('registered_by', sa.Integer(), nullable=True),
    sa.Column('last_updated_by', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['last_updated_by'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['registered_by'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('individuo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cns', sa.String(length=60), nullable=True),
    sa.Column('cpf', sa.String(length=60), nullable=True),
    sa.Column('domicilio', sa.String(length=60), nullable=True),
    sa.Column('nome', sa.String(length=60), nullable=True),
    sa.Column('nome_social', sa.String(length=60), nullable=True),
    sa.Column('data_nascimento', sa.Date(), nullable=True),
    sa.Column('sexo', sa.String(length=1), nullable=True),
    sa.Column('raca_cor', sa.String(length=60), nullable=True),
    sa.Column('etnia', sa.String(length=60), nullable=True),
    sa.Column('nome_mae', sa.String(length=60), nullable=True),
    sa.Column('nome_pai', sa.String(length=60), nullable=True),
    sa.Column('nacionalidade', sa.String(length=60), nullable=True),
    sa.Column('pais', sa.String(length=60), nullable=True),
    sa.Column('data_naturalizacao', sa.Date(), nullable=True),
    sa.Column('naturalizacao_portaria', sa.String(length=20), nullable=True),
    sa.Column('municipio_nascimento', sa.String(length=60), nullable=True),
    sa.Column('uf_nascimento', sa.String(length=2), nullable=True),
    sa.Column('entrada_brasil_data', sa.Date(), nullable=True),
    sa.Column('celular', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('relacao_responsavel', sa.String(length=60), nullable=True),
    sa.Column('ocupacao', sa.String(length=60), nullable=True),
    sa.Column('frequenta_escola_creche', sa.Boolean(), nullable=True),
    sa.Column('escolaridade', sa.String(length=60), nullable=True),
    sa.Column('situacao_mercado_trabalho', sa.String(length=60), nullable=True),
    sa.Column('frequenta_cuidador', sa.Boolean(), nullable=True),
    sa.Column('participa_grupo_comunitario', sa.Boolean(), nullable=True),
    sa.Column('plano_saude', sa.Boolean(), nullable=True),
    sa.Column('membro_povo_comunidade_tradicional', sa.Boolean(), nullable=True),
    sa.Column('orientacao_sexual', sa.String(length=60), nullable=True),
    sa.Column('identidade_genero', sa.String(length=60), nullable=True),
    sa.Column('motivo_saida', sa.String(length=60), nullable=True),
    sa.Column('data_saida', sa.Date(), nullable=True),
    sa.Column('numero_declaracao_obito', sa.String(length=15), nullable=True),
    sa.Column('gestante', sa.Boolean(), nullable=True),
    sa.Column('maternidade_referencia', sa.String(length=60), nullable=True),
    sa.Column('fumante', sa.Boolean(), nullable=True),
    sa.Column('uso_alcool', sa.Boolean(), nullable=True),
    sa.Column('uso_drogas', sa.Boolean(), nullable=True),
    sa.Column('hipertensao', sa.Boolean(), nullable=True),
    sa.Column('diabetes', sa.Boolean(), nullable=True),
    sa.Column('avc_derrame', sa.Boolean(), nullable=True),
    sa.Column('infarto', sa.Boolean(), nullable=True),
    sa.Column('doenca_cardiaca', sa.Boolean(), nullable=True),
    sa.Column('problemas_renais', sa.Boolean(), nullable=True),
    sa.Column('hanseniase', sa.Boolean(), nullable=True),
    sa.Column('doenca_respiratoria', sa.Boolean(), nullable=True),
    sa.Column('tuberculose', sa.Boolean(), nullable=True),
    sa.Column('cancer', sa.Boolean(), nullable=True),
    sa.Column('internacao_recente', sa.Boolean(), nullable=True),
    sa.Column('internacao_motivo', sa.String(length=60), nullable=True),
    sa.Column('diagnostico_problema_mental', sa.Boolean(), nullable=True),
    sa.Column('acamado', sa.Boolean(), nullable=True),
    sa.Column('domiciliado', sa.Boolean(), nullable=True),
    sa.Column('praticas_ingestivas_complementares', sa.Boolean(), nullable=True),
    sa.Column('registered_by', sa.Integer(), nullable=True),
    sa.Column('last_updated_by', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['last_updated_by'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['registered_by'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cuidador_individuo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=True),
    sa.Column('cuidador', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domicilio_animal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('domicilio_id', sa.Integer(), nullable=True),
    sa.Column('animal', sa.String(length=60), nullable=True),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['domicilio_id'], ['domicilio.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domicilio_individuo',
    sa.Column('domicilio_id', sa.Integer(), nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=False),
    sa.Column('data_residencia', sa.Date(), nullable=True),
    sa.Column('mudou', sa.Boolean(), nullable=True),
    sa.Column('renda_familia_salario_minimos', mysql.DECIMAL(), nullable=True),
    sa.Column('n_membros_familia', sa.Integer(), nullable=True),
    sa.Column('responsavel', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['domicilio_id'], ['domicilio.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('domicilio_id', 'individuo_id')
    )
    op.create_table('individuo_condicao_rua',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=True),
    sa.Column('tempo', sa.String(length=60), nullable=True),
    sa.Column('recebe_beneficio', sa.Boolean(), nullable=True),
    sa.Column('referencia_familiar', sa.Boolean(), nullable=True),
    sa.Column('refeicoes_dia', sa.Integer(), nullable=True),
    sa.Column('visita_familiar', sa.Boolean(), nullable=True),
    sa.Column('graus_parentesco_familiar', sa.String(length=20), nullable=True),
    sa.Column('instituicao_apoio', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('individuo_deficiencia',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=True),
    sa.Column('deficiencia', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('individuo_doenca_cardiaca',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=True),
    sa.Column('doenca', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('individuo_doenca_renal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=True),
    sa.Column('doenca', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('individuo_doenca_respiratoria',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('individuo_id', sa.Integer(), nullable=True),
    sa.Column('doenca', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['individuo_id'], ['individuo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('condicao_rua_acesso_higiene',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('condicao_rua_id', sa.Integer(), nullable=True),
    sa.Column('acesso_higiene', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['condicao_rua_id'], ['individuo_condicao_rua.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('condicao_rua_origem_alimentacao',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('condicao_rua_id', sa.Integer(), nullable=True),
    sa.Column('origem', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['condicao_rua_id'], ['individuo_condicao_rua.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user', 'role',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('condicao_rua_origem_alimentacao')
    op.drop_table('condicao_rua_acesso_higiene')
    op.drop_table('individuo_doenca_respiratoria')
    op.drop_table('individuo_doenca_renal')
    op.drop_table('individuo_doenca_cardiaca')
    op.drop_table('individuo_deficiencia')
    op.drop_table('individuo_condicao_rua')
    op.drop_table('domicilio_individuo')
    op.drop_table('domicilio_animal')
    op.drop_table('cuidador_individuo')
    op.drop_table('individuo')
    op.drop_table('domicilio')
    # ### end Alembic commands ###
