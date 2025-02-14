"""analitic control numeric

Revision ID: dd76798ba7c7
Revises: b663ea011b11
Create Date: 2025-02-13 16:34:38.930544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd76798ba7c7'
down_revision: Union[str, None] = 'b663ea011b11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('analitic_control', 'temperature',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=False)
    op.alter_column('analitic_control', 'ph',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=False)
    op.alter_column('analitic_control', 'color',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=False)
    op.alter_column('analitic_control', 'chlorine',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=True)
    op.alter_column('analitic_control', 'aluminum',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=False)
    op.alter_column('analitic_control', 'turbidity',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=False)
    op.alter_column('analitic_control', 'chlorides',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=10, scale=5),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('analitic_control', 'chlorides',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('analitic_control', 'turbidity',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('analitic_control', 'aluminum',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('analitic_control', 'chlorine',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('analitic_control', 'color',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('analitic_control', 'ph',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('analitic_control', 'temperature',
               existing_type=sa.Numeric(precision=10, scale=5),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
