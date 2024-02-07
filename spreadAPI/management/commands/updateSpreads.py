import logging
from spreadAPI.models import MarketSpread
from spreadAPI.serializers import UpdateMarketSpreadSerializer
from requests import get
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util


logger = logging.getLogger(__name__)


def update_spread() -> None:
    markets = get('https://www.buda.com/api/v2/markets').json()['markets']
    for market in markets:
        market_id = market['id'].lower()
        ticker = get(f'https://www.buda.com/api/v2/markets/{market_id}/ticker').json()['ticker']
        spread = round(float(ticker['min_ask'][0]) - float(ticker['max_bid'][0]), 2)
        spread_object, created = MarketSpread.objects.get_or_create(
            market = market_id,
            defaults = {
                'spread': spread
            }
        )
        data = {'spread': spread}
        serializer = UpdateMarketSpreadSerializer(spread_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
  

class Command(BaseCommand):
    help = "Runs APScheduler spread fetch script"

    def handle(self, *args, **options):
        if 'scheduler' in options:
            scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
            cron_trigger = CronTrigger(second="00")
        else:
            update_spread()
            return

        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            update_spread,
            trigger=cron_trigger,
            id="update_spread",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'update_spread'.")
        
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
