"""create_quality_table

Revision ID: a7feec4e1e59
Revises: 84d082633c32
Create Date: 2025-06-06 11:37:39.123762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7feec4e1e59'
down_revision: Union[str, None] = '84d082633c32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa
#from sqlalchemy.dialects import postgresql

def upgrade():
    # 1. Створюємо нову таблицю wind
    op.create_table(
        'air_quality',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('weather_id', sa.Integer, sa.ForeignKey('weather.id'), nullable=False),
        sa.Column('air_quality_PM2_5', sa.Float),
        sa.Column('air_quality_PM10', sa.Float),
        sa.Column('air_quality_Carbon_Monoxide', sa.Float),
        sa.Column('air_quality_Ozone', sa.Float),
        sa.Column('air_quality_Nitrogen_dioxide', sa.Float),
        sa.Column('air_quality_Sulphur_dioxide', sa.Float)
    )
    
    # 2. Переносимо дані з weather до air_quality
    connection = op.get_bind()
    
    # Отримуємо всі дані з weather
    results = connection.execute(
    sa.text('SELECT id, "air_quality_PM2_5", "air_quality_PM10", "air_quality_Carbon_Monoxide", "air_quality_Ozone", "air_quality_Nitrogen_dioxide", "air_quality_Sulphur_dioxide" FROM weather')
    ).fetchall()

    
    # Вставляємо дані в нову таблицю air_quality
    for row in results:
        connection.execute(
            sa.text(
                'INSERT INTO air_quality (weather_id, "air_quality_PM2_5", "air_quality_PM10", "air_quality_Carbon_Monoxide", "air_quality_Ozone", "air_quality_Nitrogen_dioxide", "air_quality_Sulphur_dioxide") '
                'VALUES (:weather_id, :air_quality_PM2_5, :air_quality_PM10, :air_quality_Carbon_Monoxide, :air_quality_Ozone, :air_quality_Nitrogen_dioxide, :air_quality_Sulphur_dioxide)'
            ),
            {
                'weather_id': row[0],
                'air_quality_PM2_5': row[1],
                'air_quality_PM10': row[2],
                'air_quality_Carbon_Monoxide': row[3],
                'air_quality_Ozone': row[4],
                'air_quality_Nitrogen_dioxide': row[5],
                'air_quality_Sulphur_dioxide': row[6]
            }
        )
    
    # 3. Додаємо булеву колонку
    op.add_column('air_quality', sa.Column('should_go_out', sa.Boolean))
    
    # 4. Заповнюємо, норми на windy порівнював
    op.execute(
        'UPDATE air_quality SET should_go_out = (("air_quality_PM2_5" < 25) AND ("air_quality_PM10" < 40) AND ("air_quality_Carbon_Monoxide" < 450) AND ("air_quality_Ozone" < 120) AND ("air_quality_Nitrogen_dioxide" < 25) AND ("air_quality_Sulphur_dioxide" < 25));'
    )
    
    # 5. Видаляємо старі колонки з weather
    op.drop_column('weather', 'air_quality_PM2_5')
    op.drop_column('weather', 'air_quality_PM10')
    op.drop_column('weather', 'air_quality_Carbon_Monoxide')
    op.drop_column('weather', 'air_quality_Ozone')
    op.drop_column('weather', 'air_quality_Nitrogen_dioxide')
    op.drop_column('weather', 'air_quality_Sulphur_dioxide')

def downgrade():
    # 1. Додаємо колонки назад до weather
    op.add_column('weather', sa.Column('air_quality_PM2_5', sa.Float))
    op.add_column('weather', sa.Column('air_quality_PM10', sa.Float))
    op.add_column('weather', sa.Column('air_quality_Carbon_Monoxide', sa.Float))
    op.add_column('weather', sa.Column('air_quality_Ozone', sa.Float))
    op.add_column('weather', sa.Column('air_quality_Nitrogen_dioxide', sa.Float))
    op.add_column('weather', sa.Column('air_quality_Sulphur_dioxide', sa.Float))
    
    # 2. Переносимо дані назад
    connection = op.get_bind()
    results = connection.execute(
        sa.text('SELECT weather_id, "air_quality_PM2_5", "air_quality_PM10", "air_quality_Carbon_Monoxide", "air_quality_Ozone", "air_quality_Nitrogen_dioxide", "air_quality_Sulphur_dioxide" FROM air_quality')
    ).fetchall()
    
    for row in results:
        connection.execute(
            sa.text(
                "UPDATE weather SET "
                "\"air_quality_PM2_5\" = :air_quality_PM2_5, "  # додаємо подвійні лапки
                "\"air_quality_PM10\" = :air_quality_PM10, "
                "\"air_quality_Carbon_Monoxide\" = :air_quality_Carbon_Monoxide, "
                "\"air_quality_Ozone\" = :air_quality_Ozone, "
                "\"air_quality_Nitrogen_dioxide\" = :air_quality_Nitrogen_dioxide, "
                "\"air_quality_Sulphur_dioxide\" = :air_quality_Sulphur_dioxide "  # тільки пробіл перед WHERE достатній
                "WHERE id = :weather_id"
            ),
            {
                'weather_id': row[0],
                'air_quality_PM2_5': row[1],
                'air_quality_PM10': row[2],
                'air_quality_Carbon_Monoxide': row[3],
                'air_quality_Ozone': row[4],
                'air_quality_Nitrogen_dioxide': row[5],
                'air_quality_Sulphur_dioxide': row[6]
            }
        )
    
    # 3. Видаляємо колонку should_go_out
    op.drop_column('air_quality', 'should_go_out')
    
    # 4. Видаляємо таблицю air_quality
    op.drop_table('air_quality')