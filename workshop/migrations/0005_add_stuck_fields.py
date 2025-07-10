# Generated manually for stuck fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_repairitem_block_notes_repairitem_block_reason_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE workshop_repairjob ADD COLUMN is_stuck BOOLEAN DEFAULT 0;",
            reverse_sql="ALTER TABLE workshop_repairjob DROP COLUMN is_stuck;"
        ),
        migrations.RunSQL(
            "ALTER TABLE workshop_repairjob ADD COLUMN stuck_reason TEXT DEFAULT '';",
            reverse_sql="ALTER TABLE workshop_repairjob DROP COLUMN stuck_reason;"
        ),
        migrations.RunSQL(
            "ALTER TABLE workshop_repairjob ADD COLUMN stuck_at DATETIME NULL;",
            reverse_sql="ALTER TABLE workshop_repairjob DROP COLUMN stuck_at;"
        ),
        migrations.RunSQL(
            "ALTER TABLE workshop_repairjob ADD COLUMN stuck_resolved BOOLEAN DEFAULT 0;",
            reverse_sql="ALTER TABLE workshop_repairjob DROP COLUMN stuck_resolved;"
        ),
        migrations.RunSQL(
            "ALTER TABLE workshop_repairjob ADD COLUMN manager_response TEXT DEFAULT '';",
            reverse_sql="ALTER TABLE workshop_repairjob DROP COLUMN manager_response;"
        ),
    ]
