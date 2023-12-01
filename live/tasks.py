from celery import shared_task

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"