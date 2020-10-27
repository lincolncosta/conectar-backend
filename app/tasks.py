from core.celery_app import celery_app

# refresh_token_list = []

@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    return f"test task returns {word}"

# @celery_app.task
# def append_refresh_token(token: str):
#     r.lpush(token)
#     return

# @celery_app.task
# def check_refresh_token(token: str) -> bool:
#     refresh_token_exists = r.lpos(token)
#     if refresh_token_exists:
#         return True
#     return False


# def append_refresh_token(token: str):
#     refresh_token_list.append(token)

# def check_refresh_token(token: str) -> bool:
#     print(refresh_token_list)
#     print(token)
#     return token in refresh_token_list