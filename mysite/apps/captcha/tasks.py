import os
from datetime import datetime

from celery.schedules import crontab
from django.conf import settings

from mysite import celery_app

captcha_dir = getattr(settings, "CAPTCHA_DIR")


@celery_app.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(
        schedule=crontab(minute="*/1"),
        sig=remove_outdated_captcha_image.s(),
        name="remove outdated captcha image",
    )

    sender.add_periodic_task(
        schedule=crontab(minute="*/1"),
        sig=debug_periodic_task.s(),
        args=("[Debug periodic task]",),
        name="debug periodic task",
    )


@celery_app.task
def remove_outdated_captcha_image():
    for this in captcha_dir.glob("*"):
        if this.is_file():
            created_time = os.path.getctime(this)  # 获取验证码图片创建的时间
            delta = datetime.now().timestamp() - created_time
            if delta >= 60:
                this.unlink()


@celery_app.task
def debug_periodic_task(args):
    print(args)
