"""Fix Post.excerpt to Text; Comment.email nullable

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-19 09:15:00.000000

NOTE: comment.is_admin and post.tags->Text were already handled in b2c3d4e5f6a7.
This migration only adds the remaining changes: excerpt->Text and email nullable.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade():
    # post.excerpt: String(300) -> Text
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('excerpt',
            existing_type=sa.String(length=300),
            type_=sa.Text(),
            existing_nullable=False
        )

    # comment.email: make nullable so admin replies (no email) can be saved
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('email',
            existing_type=sa.String(length=100),
            nullable=True
        )


def downgrade():
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('email',
            existing_type=sa.String(length=100),
            nullable=False
        )

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('excerpt',
            existing_type=sa.Text(),
            type_=sa.String(length=300),
            existing_nullable=False
        )
