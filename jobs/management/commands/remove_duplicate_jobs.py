from django.core.management.base import BaseCommand
from jobs.models import Job
from collections import defaultdict

class Command(BaseCommand):
    help = 'Remove duplicate Job entries based on title, company, and location.'

    def handle(self, *args, **options):
        duplicates = defaultdict(list)
        for job in Job.objects.all():
            key = (job.title.strip().lower(), job.company_id, job.location.strip().lower())
            duplicates[key].append(job.id)
        total_removed = 0
        for key, ids in duplicates.items():
            if len(ids) > 1:
                # keep the first, delete the rest
                keep_id = ids[0]
                to_delete = ids[1:]
                Job.objects.filter(id__in=to_delete).delete()
                total_removed += len(to_delete)
                self.stdout.write(f"Removed {len(to_delete)} duplicate(s) for job '{key[0]}' at company ID {key[1]}.")
        self.stdout.write(self.style.SUCCESS(f"Finished. Total duplicates removed: {total_removed}"))
