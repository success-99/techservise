from background_task import background
from remove import delete_expired_tokens


@background(schedule=60)
def delete_expired_tokens_daily(sender, **kwargs):
    return delete_expired_tokens()
