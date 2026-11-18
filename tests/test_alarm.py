
import unittest
from datetime import datetime, time

from alarm_clock.alarm import Alarm


class TestAlarm(unittest.TestCase):

    def test_create_alarm(self):
        alarm = Alarm.create("18:30")
        self.assertEqual(alarm.alarm_time.hour, 18)
        self.assertEqual(alarm.alarm_time.minute, 30)

    def test_invalid_time(self):
        with self.assertRaises(ValueError):
            Alarm.create("25:90")

    def test_rejects_single_digit_hour(self):
        with self.assertRaises(ValueError):
            Alarm.create("5:53")

    def test_rejects_invalid_minutes(self):
        with self.assertRaises(ValueError):
            Alarm.create("18:75")

    def test_rejects_invalid_hour(self):
        with self.assertRaises(ValueError):
            Alarm.create("25:30")

    def test_accepts_midnight(self):
        alarm = Alarm.create("00:00")
        self.assertEqual(alarm.alarm_time, time(0, 0))

    def test_start_ringing(self):
        alarm = Alarm.create("18:30")
        alarm.start_ringing()
        self.assertTrue(alarm.ringing)

    def test_stop_ringing(self):
        alarm = Alarm.create("18:30")
        alarm.start_ringing()
        alarm.stop_ringing()

        self.assertFalse(alarm.ringing)
        self.assertFalse(alarm.enabled)

    def test_snooze(self):
        alarm = Alarm.create("18:30")
        alarm.start_ringing()

        now = datetime(2026, 11, 18, 18, 30)
        alarm.snooze(5, now)

        self.assertEqual(
            alarm.snoozed_until,
            datetime(2026, 11, 18, 18, 35)
        )
        self.assertFalse(alarm.ringing)
        self.assertTrue(alarm.enabled)

    def test_snooze_across_midnight(self):
        alarm = Alarm.create("23:58")
        alarm.start_ringing()

        now = datetime(2026, 11, 18, 23, 58)
        alarm.snooze(5, now)

        self.assertEqual(
            alarm.snoozed_until,
            datetime(2026, 11, 19, 0, 3)
        )

    def test_invalid_snooze_duration(self):
        alarm = Alarm.create("18:30")
        alarm.start_ringing()

        with self.assertRaises(ValueError):
            alarm.snooze(0)

    def test_snooze_when_not_ringing(self):
        alarm = Alarm.create("18:30")

        with self.assertRaises(ValueError):
            alarm.snooze(5)


if __name__ == "__main__":
    unittest.main()
