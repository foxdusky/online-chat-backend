"""init migration

Revision ID: 3e439191166e
Revises: 
Create Date: 2024-10-22 23:35:36.671300

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3e439191166e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('user_count', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('reg_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('message',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('chat_id', sa.Integer(), nullable=False),
                    sa.Column('sent_at', sa.DateTime(), nullable=True),
                    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users_in_chat',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('chat_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('message_action',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('message_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('done_at', sa.DateTime(), nullable=True),
                    sa.Column('action', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.execute("""
        INSERT INTO "user" ("username", "password")
        VALUES (
            'duskyfox',
            '$2b$12$GOhdYrYrq1Q79MkUkh7n2u6n7gFVNT.7wI16lDz5h8/Kpk1f46d5W'
        )
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_action')
    op.drop_table('users_in_chat')
    op.drop_table('message')
    op.drop_table('user')
    op.drop_table('chat')
    # ### end Alembic commands ###
