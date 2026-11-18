
import threading
import time
from datetime import datetime

from alarm_clock.alarm import Alarm


class AlarmScheduler:

    def __init__(self):
        self.alarms: dict[str, Alarm] = {}
        self.running = False
        self.lock = threading.Lock()

    def add_alarm(self, alarm: Alarm) -> None:
        with self.lock:
            self.alarms[alarm.id] = alarm

    def remove_alarm(self, alarm_id: str) -> bool:
        with self.lock:
            if alarm_id not in self.alarms:
                return False

            del self.alarms[alarm_id]
            return True

    def list_alarms(self) -> list[Alarm]:
        with self.lock:
            return list(self.alarms.values())

    def check_alarms(
        self,
        current_time: datetime | None = None
    ) -> list[Alarm]:
        """Check normal and snoozed alarms."""
        now = current_time or datetime.now()
        triggered = []

        with self.lock:
            for alarm in self.alarms.values():

                if not alarm.enabled or alarm.ringing:
                    continue

                # Check snoozed alarms first.
                if alarm.snoozed_until is not None:
                    if now >= alarm.snoozed_until:
                        alarm.snoozed_until = None
                        alarm.start_ringing()
                        triggered.append(alarm)

                    continue

                # Check regular alarms.
                if (
                    alarm.alarm_time.hour == now.hour
                    and alarm.alarm_time.minute == now.minute
                ):
                    alarm.start_ringing()
                    triggered.append(alarm)

        return triggered

    def run(self):
        self.running = True

        while self.running:
            triggered = self.check_alarms()

            for alarm in triggered:
                print(
                    f"\n🔔 ALARM! Alarm {alarm.id} is ringing!"
                )

            time.sleep(1)

    def stop(self):
        self.running = False
