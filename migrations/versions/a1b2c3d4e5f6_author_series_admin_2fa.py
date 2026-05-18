"""Add Author, PostSeries, PostSeriesEntry tables; add admin 2FA columns and post author_id

Revision ID: a1b2c3d4e5f6
Revises: 0f28bee38e6a
Create Date: 2026-05-18 09:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '0f28bee38e6a'
branch_labels = None
depends_on = None


def upgrade():
    # ── Author table ──────────────────────────────────────────────────────────
    op.create_table('author',
        sa.Column('id',      sa.Integer(), nullable=False),
        sa.Column('name',    sa.String(length=100), nullable=False),
        sa.Column('slug',    sa.String(length=120), nullable=False),
        sa.Column('bio',     sa.Text(), nullable=True),
        sa.Column('avatar',  sa.String(length=500), nullable=True),
        sa.Column('email',   sa.String(length=150), nullable=True),
        sa.Column('twitter', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # ── PostSeries table ──────────────────────────────────────────────────────
    op.create_table('post_series',
        sa.Column('id',          sa.Integer(), nullable=False),
        sa.Column('title',       sa.String(length=200), nullable=False),
        sa.Column('slug',        sa.String(length=220), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at',  sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # ── PostSeriesEntry table ─────────────────────────────────────────────────
    op.create_table('post_series_entry',
        sa.Column('id',        sa.Integer(), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=False),
        sa.Column('post_id',   sa.Integer(), nullable=False),
        sa.Column('position',  sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'],   ['post.id']),
        sa.ForeignKeyConstraint(['series_id'], ['post_series.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # ── Add author_id FK to post ──────────────────────────────────────────────
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_post_author', 'author', ['author_id'], ['id'])

    # ── Add 2FA columns to admin ──────────────────────────────────────────────
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('totp_secret',  sa.String(length=32), nullable=True))
         expression
        batch_op.add_column(sa.Column('totp_enabled', sa.Boolean(), nullable=False,
                                      server_default=sa.false()))

def downgrade():
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('totp_enabled')
        batch_op.drop_column('totp_secret')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_author', type_='foreignkey')
        batch_op.drop_column('author_id')

    op.drop_table('post_series_entry')
    op.drop_table('post_series')
    op.drop_table('author')
