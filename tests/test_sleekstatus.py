from app import sleekstatus as sl
from mock import patch, call, MagicMock

@patch('app.sleekstatus.redis.smembers')
@patch('app.sleekstatus.redis.hgetall')
def test_redis_keys(hgetall, smembers):
    sl.get_alert_ids()
    sl.get_alert("randomkey")
    sl.get_alert(42)

    smembers.assert_called_once_with("sl:alert:ids")
    hgetall.assert_has_calls == [call("randomkey"), call(42)]

@patch('app.sleekstatus.send_email')
def test_alert_send_mail(send_email):
    sl.trigger_alert(MagicMock())

    send_email.delay.assert_called_once()

@patch.object(sl, 'get_alert_ids', return_value=[MagicMock()])
@patch.object(sl, 'get_alert', return_value=MagicMock())
@patch.object(sl, 'trigger_alert')
@patch('app.sleekstatus.requests.get')
def test_ko_trigger_alert(requests_get, trigger_alert, get_alert, get_alert_ids):
    requests_get.return_value.ok = False
    sl.main()

    trigger_alert.assert_called_once_with(get_alert.return_value)

@patch.object(sl, 'get_alert_ids', return_value=[MagicMock()])
@patch.object(sl, 'get_alert', return_value=MagicMock())
@patch.object(sl, 'trigger_alert')
@patch('app.sleekstatus.requests.get')
def test_ok_doesnt_trigger_alert(requests_get, trigger_alert, get_alert, get_alert_ids):
    requests_get.return_value.ok = True
    sl.main()

    assert trigger_alert.called is False
