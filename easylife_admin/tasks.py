from celery import shared_task

from time import sleep
@shared_task
def sleepy(duration):
	sleep(duration)
	return True


@shared_task
def mul(x, y):
    return x * y
