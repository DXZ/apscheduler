"""
This example demonstrates the use of the Redis job store.
On each run, it adds a new alarm that fires after ten seconds.
You can exit the program, restart it and observe that any previous alarms that have not fired yet are still active.
Running the example with the --clear switch will remove any existing alarms.
"""

from datetime import datetime, timedelta
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore


def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    jobstore = RedisJobStore(jobs_key='example.jobs', run_times_key='example.run_times')
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        jobstore.remove_all_jobs()

    scheduler.add_jobstore(jobstore)
    alarm_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(alarm, 'date', run_date=alarm_time, args=[datetime.now()])
    print('To clear the alarms, run this example with the --clear argument.')
    print('Press Ctrl+C to exit')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
