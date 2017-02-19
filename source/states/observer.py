

class Observer(object):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.subscribers = set()

    def add_subscriber(self, subscriber):
        self.subscribers.add(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def send_report(self, report):
        for subscriber in self.subscribers:
            subscriber.receive_report(report)


class ReporterComponent(object):

    """Units in battle will get reporter components and send reports relating changes in the battle
    state to the battle scale"""

    def __init__(self, observer):
        self.observer = observer

    def send_report(self, report_type, *args):
        report = Report(report_type, *args)
        self.observer.send_report(report)


class Report(object):

    def __init__(self, report_type, *args):

        self.report_type = report_type
        self.args = args
