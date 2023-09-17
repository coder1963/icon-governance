"""v0.4.1-public-key

Revision ID: 5fd584cbb64d
Revises: 9e1abdbf7641
Create Date: 2023-09-17 01:22:23.837512

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "5fd584cbb64d"
down_revision = "9e1abdbf7641"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "preps", sa.Column("public_key", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("preps", "public_key")
    # ### end Alembic commands ###