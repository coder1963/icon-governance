"""v0.7.0-iiss4-preps

Revision ID: 76a52d8cadde
Revises: b2bff849e370
Create Date: 2023-12-27 12:33:56.369370

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "76a52d8cadde"
down_revision = "b2bff849e370"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("apy_time", sa.Column("i_wage", sa.Float(), nullable=True))
    op.alter_column(
        "apy_time",
        "i_voter",
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.add_column(
        "preps", sa.Column("jail_flags", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )
    op.add_column("preps", sa.Column("unjail_request_height", sa.Integer(), nullable=True))
    op.add_column("preps", sa.Column("max_commission_change_rate", sa.Float(), nullable=True))
    op.add_column("preps", sa.Column("max_commission_rate", sa.Float(), nullable=True))
    op.add_column("preps", sa.Column("commission_rate", sa.Float(), nullable=True))
    op.add_column("preps", sa.Column("min_double_sign_height", sa.Integer(), nullable=True))
    op.add_column("preps", sa.Column("has_public_key", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("preps", "has_public_key")
    op.drop_column("preps", "min_double_sign_height")
    op.drop_column("preps", "commission_rate")
    op.drop_column("preps", "max_commission_rate")
    op.drop_column("preps", "max_commission_change_rate")
    op.drop_column("preps", "unjail_request_height")
    op.drop_column("preps", "jail_flags")
    op.alter_column(
        "apy_time",
        "i_voter",
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.drop_column("apy_time", "i_wage")
    # ### end Alembic commands ###