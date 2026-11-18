
import re
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from uuid import uuid4


@dataclass
class Alarm:
    alarm_time: time
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    enabled: bool = True
    ringing: bool = False
    snoozed_until: datetime | None = None

    @classmethod
    def create(cls, time_string: str) -> "Alarm":
        """Create an alarm using strict HH:MM format."""

        if not re.fullmatch(
            r"(?:[01]\d|2[0-3]):[0-5]\d",
            time_string
        ):
            raise ValueError("Invalid time. Use HH:MM format.")

        return cls(alarm_time=time.fromisoformat(time_string))

    def start_ringing(self) -> None:
        if self.enabled:
            self.ringing = True

    def stop_ringing(self) -> None:
        """Dismiss the alarm."""
        self.ringing = False
        self.enabled = False
        self.snoozed_until = None

    def snooze(
        self,
        minutes: int = 5,
        now: datetime | None = None
    ) -> None:
        """Postpone a ringing alarm."""

        if minutes <= 0:
            raise ValueError("Snooze duration must be positive.")

        if not self.ringing:
            raise ValueError("Alarm is not currently ringing.")

        current_time = now or datetime.now()

        self.snoozed_until = current_time + timedelta(
            minutes=minutes
        )

        self.ringing = False
        self.enabled = True
