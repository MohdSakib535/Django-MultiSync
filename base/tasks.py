from celery import shared_task
from .models import Record, SyncStatus

@shared_task
def sync_to_read_database(record_id):
    """
    Copies a record from MySQL (default DB) to PostgreSQL (read DB).
    """
    try:
        # Fetch the record from MySQL (default DB)
        record = Record.objects.using('default').get(id=record_id)

        # Insert the record into PostgreSQL (read DB)
        Record.objects.using('read_db').update_or_create(
            id=record.id,  # Ensure same ID
            defaults={'title': record.title, 'description': record.description, 'synced': True}
        )

        # Mark the record as synced in MySQL
        record.synced = True
        record.save(using='default')

        return f"Record {record_id} successfully synced."

    except Record.DoesNotExist:
        return f"Record {record_id} not found in MySQL."

    except Exception as e:
        return f"Error syncing record {record_id}: {str(e)}"

@shared_task
def sync_unsynced_records():
    """
    Periodically checks for records in MySQL that haven't been synced to PostgreSQL.
    """
    unsynced_records = Record.objects.using('default').filter(synced=False)
    for record in unsynced_records:
        sync_to_read_database.delay(record.id)  # Trigger sync for each record