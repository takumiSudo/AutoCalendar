import unittest
from src.services.base_event_manager import GoogleEventsManager
from src.utils.event_class import DataLoader

class TestGoogleEventsManager(unittest.TestCase):

    def setUp(self):
        self.events_manager = GoogleEventsManager()

    def test_create_event_valid(self):
        summary = "Meeting with Alice"
        start_time = "2025-01-10T12:00:00"
        end_time = "2025-01-10T13:00:00"
        description = "Discuss project updates"
        location = "Conference Room B"
        self.events_manager.create_event(summary, start_time, end_time, description, location)
        # Check the output manually to ensure the event is created

    def test_create_event_invalid_time_format(self):
        summary = "Meeting with Charlie"
        start_time = "2025-01-10 12:00:00"  # Invalid format
        end_time = "2025-01-10 13:00:00"    # Invalid format
        description = "Discuss project updates"
        location = "Conference Room C"
        self.events_manager.create_event(summary, start_time, end_time, description, location)
        # Check the output manually to ensure the time format is fixed and the event is created

    def test_create_event_end_time_before_start_time(self):
        summary = "Meeting with Eve"
        start_time = "2025-01-10T14:00:00"
        end_time = "2025-01-10T13:00:00"  # End time before start time
        description = "Discuss project updates"
        location = "Conference Room D"
        self.events_manager.create_event(summary, start_time, end_time, description, location)
        # Check the output manually to ensure the event is not created due to invalid time order

class TestDataLoader(unittest.TestCase):

    def test_check_time_format_valid(self):
        data_loader = DataLoader("Test Event", "2025-01-10T12:00:00", "2025-01-10T13:00:00")
        self.assertTrue(data_loader.check_time_format(data_loader.start_time))
        self.assertTrue(data_loader.check_time_format(data_loader.end_time))

    def test_check_time_format_invalid(self):
        data_loader = DataLoader("Test Event", "2025-01-10 12:00:00", "2025-01-10 13:00:00")
        self.assertFalse(data_loader.check_time_format(data_loader.start_time))
        self.assertFalse(data_loader.check_time_format(data_loader.end_time))

    def test_fix_time_format(self):
        data_loader = DataLoader("Test Event", "2025-01-10 12:00:00", "2025-01-10 13:00:00")
        fixed_start_time = data_loader.fix_time_format(data_loader.start_time)
        fixed_end_time = data_loader.fix_time_format(data_loader.end_time)
        self.assertEqual(fixed_start_time, "2025-01-10T12:00:00")
        self.assertEqual(fixed_end_time, "2025-01-10T13:00:00")

    def test_check_time_order_valid(self):
        data_loader = DataLoader("Test Event", "2025-01-10T12:00:00", "2025-01-10T13:00:00")
        self.assertTrue(data_loader.check_time_order(data_loader.start_time, data_loader.end_time))

    def test_check_time_order_invalid(self):
        data_loader = DataLoader("Test Event", "2025-01-10T14:00:00", "2025-01-10T13:00:00")
        self.assertFalse(data_loader.check_time_order(data_loader.start_time, data_loader.end_time))

if __name__ == "__main__":
    unittest.main()