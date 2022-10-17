import pytest


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'redis://'
    }


# def test_add(celery_worker):
#     mytask.delay()


@pytest.fixture(scope='session')
def celery_enable_logging():
    return True
