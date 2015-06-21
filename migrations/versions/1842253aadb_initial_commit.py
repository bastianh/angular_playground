"""initial commit

Revision ID: 1842253aadb
Revises: None
Create Date: 2015-06-20 11:22:23.193457

"""

# revision identifiers, used by Alembic.
revision = '1842253aadb'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_api_calls',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('params', postgresql.JSON(), nullable=True),
    sa.Column('success', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('result_timestamp', sa.DateTime(), nullable=True),
    sa.Column('result_expires', sa.DateTime(), nullable=True),
    sa.Column('apikey_id', sa.Integer(), nullable=True),
    sa.Column('api_error_code', sa.Integer(), nullable=True),
    sa.Column('api_error_message', sa.String(), nullable=True),
    sa.Column('http_error_code', sa.Integer(), nullable=True),
    sa.Column('http_error_message', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_api_calls_created'), 'app_api_calls', ['created'], unique=False)
    op.create_index(op.f('ix_app_api_calls_path'), 'app_api_calls', ['path'], unique=False)
    op.create_index(op.f('ix_app_api_calls_success'), 'app_api_calls', ['success'], unique=False)
    op.create_table('app_user',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.Column('provider_name', sa.String(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('character_name', sa.String(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('character_id')
    )
    op.create_index('provider', 'app_user', ['provider_id', 'provider_name'], unique=True)
    op.create_table('prx_todo',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('creator_id', postgresql.UUID(), nullable=False),
    sa.Column('task', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['app_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prx_todo')
    op.drop_index('provider', table_name='app_user')
    op.drop_table('app_user')
    op.drop_index(op.f('ix_app_api_calls_success'), table_name='app_api_calls')
    op.drop_index(op.f('ix_app_api_calls_path'), table_name='app_api_calls')
    op.drop_index(op.f('ix_app_api_calls_created'), table_name='app_api_calls')
    op.drop_table('app_api_calls')
    ### end Alembic commands ###
