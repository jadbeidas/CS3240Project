from .models import Report

# returns number of reports in the database
def get_report_count():
    return Report.objects.count()

# returns number of completed reports in the database
def get_completed_reports_count():
    return Report.objects.filter(status=2).count()
# returns number of in progress reports in the database
def get_in_progress_reports_count():
    return Report.objects.filter(status=1).count()

def get_new_reports_count():
    return Report.objects.filter(status=0).count()

def get_pending_reports_count():
    pending = get_in_progress_reports_count() + get_new_reports_count()
    return pending

def mark_report_in_progress(report):
    report.status = 1
    report.save()

def mark_report_completed(report):
    report.status = 2
    report.save()