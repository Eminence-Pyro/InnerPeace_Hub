"""Fix tags column: String(300) -> Text; add comment.is_admin; add PostSeriesEntry.post_id cascade

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-19 05:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Fix tags column — remove 300 char limit
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('tags',
            existing_type=sa.String(length=300),
            type_=sa.Text(),
            existing_nullable=True
        )

    # Add is_admin flag to comment
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('is_admin', sa.Boolean(), nullable=False,
                      server_default=sa.text('false'))
        )


def downgrade():
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('tags',
            existing_type=sa.Text(),
            type_=sa.String(length=300),
            existing_nullable=True
        )
