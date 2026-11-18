
import threading

from alarm_clock.alarm import Alarm
from alarm_clock.scheduler import AlarmScheduler


class AlarmCLI:

    def __init__(self):
        self.scheduler = AlarmScheduler()

        self.scheduler_thread = threading.Thread(
            target=self.scheduler.run,
            daemon=True
        )
        self.scheduler_thread.start()

    def add_alarm(self):
        time_string = input("Enter alarm time (HH:MM): ")

        try:
            alarm = Alarm.create(time_string)
            self.scheduler.add_alarm(alarm)
            print(f"Alarm created successfully. ID: {alarm.id}")

        except ValueError as error:
            print(f"Error: {error}")

    def list_alarms(self):
        alarms = self.scheduler.list_alarms()

        if not alarms:
            print("No alarms found.")
            return

        for alarm in alarms:
            status = "Ringing" if alarm.ringing else (
                "Enabled" if alarm.enabled else "Disabled"
            )

            print(
                f"ID: {alarm.id} | "
                f"Time: {alarm.alarm_time.strftime('%H:%M')} | "
                f"Status: {status}"
            )

            if alarm.snoozed_until:
                print(
                    f"  Snoozed until: "
                    f"{alarm.snoozed_until.strftime('%Y-%m-%d %H:%M')}"
                )

    def find_alarm(self, alarm_id):
        for alarm in self.scheduler.list_alarms():
            if alarm.id == alarm_id:
                return alarm

        return None

    def delete_alarm(self):
        alarm_id = input("Enter alarm ID: ")

        if self.scheduler.remove_alarm(alarm_id):
            print("Alarm deleted successfully.")
        else:
            print("Alarm not found.")

    def snooze_alarm(self):
        alarm_id = input("Enter ringing alarm ID: ")
        alarm = self.find_alarm(alarm_id)

        if alarm is None:
            print("Alarm not found.")
            return

        duration = input("Snooze duration in minutes (default 5): ").strip()

        try:
            minutes = int(duration) if duration else 5
            alarm.snooze(minutes)
            print(f"Alarm snoozed for {minutes} minutes.")

        except ValueError as error:
            print(f"Error: {error}")

    def dismiss_alarm(self):
        alarm_id = input("Enter ringing alarm ID: ")
        alarm = self.find_alarm(alarm_id)

        if alarm is None:
            print("Alarm not found.")
            return

        if not alarm.ringing:
            print("This alarm is not currently ringing.")
            return

        alarm.stop_ringing()
        print("Alarm dismissed successfully.")

    def run(self):
        try:
            while True:
                print("\n===== PYTHON ALARM CLOCK =====")
                print("1. Add Alarm")
                print("2. List Alarms")
                print("3. Delete Alarm")
                print("4. Snooze Alarm")
                print("5. Dismiss Alarm")
                print("6. Exit")

                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self.add_alarm()
                elif choice == "2":
                    self.list_alarms()
                elif choice == "3":
                    self.delete_alarm()
                elif choice == "4":
                    self.snooze_alarm()
                elif choice == "5":
                    self.dismiss_alarm()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")

        finally:
            self.scheduler.stop()
            self.scheduler_thread.join(timeout=2)
