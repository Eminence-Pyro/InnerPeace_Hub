"""Fix Post.tags/excerpt to Text; add Comment.is_admin; Comment.email nullable

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-19 09:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('tags',
            existing_type=sa.String(length=200),
            type_=sa.Text(),
            existing_nullable=True
        )
        batch_op.alter_column('excerpt',
            existing_type=sa.String(length=300),
            type_=sa.Text(),
            existing_nullable=False
        )

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('is_admin', sa.Boolean(), nullable=False,
                      server_default=sa.text('false'))
        )
        batch_op.alter_column('email',
            existing_type=sa.String(length=100),
            nullable=True
        )


def downgrade():
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('is_admin')
        batch_op.alter_column('email', existing_type=sa.String(length=100), nullable=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('excerpt', existing_type=sa.Text(), type_=sa.String(300), existing_nullable=False)
        batch_op.alter_column('tags', existing_type=sa.Text(), type_=sa.String(200), existing_nullable=True)
