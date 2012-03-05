

from daemon import Daemon

class ReportNotifier(Daemon):
    def run(self):
        print 'stuff'

from django.conf import settings

report_notifier = ReportNotifier(settings.REPORT_NOTIFIER_PID)
report_notifier.start()

# export PYTHONPATH=${PYTHONPATH}:/var/www/sites/odcdn/opendream.in.th/subdomains/sms/sources