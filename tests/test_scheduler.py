
import unittest
from datetime import datetime

from alarm_clock.alarm import Alarm
from alarm_clock.scheduler import AlarmScheduler


class TestAlarmScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = AlarmScheduler()

    def test_add_alarm(self):
        alarm = Alarm.create("10:30")
        self.scheduler.add_alarm(alarm)

        self.assertEqual(len(self.scheduler.list_alarms()), 1)

    def test_remove_alarm(self):
        alarm = Alarm.create("10:30")
        self.scheduler.add_alarm(alarm)

        result = self.scheduler.remove_alarm(alarm.id)

        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.list_alarms()), 0)

    def test_trigger_alarm(self):
        alarm = Alarm.create("10:30")
        self.scheduler.add_alarm(alarm)

        now = datetime(2026, 11, 18, 10, 30)
        triggered = self.scheduler.check_alarms(now)

        self.assertEqual(len(triggered), 1)
        self.assertTrue(alarm.ringing)

    def test_alarm_does_not_trigger_twice(self):
        alarm = Alarm.create("10:30")
        self.scheduler.add_alarm(alarm)

        now = datetime(2026, 11, 18, 10, 30)

        first = self.scheduler.check_alarms(now)
        second = self.scheduler.check_alarms(now)

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 0)

    def test_snoozed_alarm_does_not_trigger_early(self):
        alarm = Alarm.create("18:30")
        alarm.start_ringing()

        alarm.snooze(5, datetime(2026, 11, 18, 18, 30))
        self.scheduler.add_alarm(alarm)

        triggered = self.scheduler.check_alarms(
            datetime(2026, 11, 18, 18, 34)
        )

        self.assertEqual(len(triggered), 0)

    def test_snoozed_alarm_triggers_at_correct_time(self):
        alarm = Alarm.create("18:30")
        alarm.start_ringing()

        alarm.snooze(5, datetime(2026, 11, 18, 18, 30))
        self.scheduler.add_alarm(alarm)

        triggered = self.scheduler.check_alarms(
            datetime(2026, 11, 18, 18, 35)
        )

        self.assertEqual(len(triggered), 1)
        self.assertTrue(alarm.ringing)
        self.assertIsNone(alarm.snoozed_until)

    def test_snoozed_alarm_triggers_after_midnight(self):
        alarm = Alarm.create("23:58")
        alarm.start_ringing()

        alarm.snooze(5, datetime(2026, 11, 18, 23, 58))
        self.scheduler.add_alarm(alarm)

        triggered = self.scheduler.check_alarms(
            datetime(2026, 11, 19, 0, 3)
        )

        self.assertEqual(len(triggered), 1)
        self.assertTrue(alarm.ringing)


if __name__ == "__main__":
    unittest.main()
