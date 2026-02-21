import logging
import time

logger = logging.getLogger(__name__)

REQUEST_RETRY_TIMES = 3

def request_with_retry(func, *args, **kwargs):
    """带重试的接口请求，避免单次请求失败导致程序中断"""
    for retry in range(REQUEST_RETRY_TIMES):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"接口请求失败，重试{retry + 1}/{REQUEST_RETRY_TIMES}，错误：{str(e)}")
            time.sleep(10)
    logger.error(f"接口请求最终失败，函数：{func.__name__}")
    return None
