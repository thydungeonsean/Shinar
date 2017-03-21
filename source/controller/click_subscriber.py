import weakref


class ClickObserver(object):

    def __init__(self):

        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def left_click(self):
        for member in self.members[:]:
            member().on_left_click(member())

    def right_click(self):
        for member in self.members[:]:
            member().on_right_click(member())


class ClickSubscriber(object):

    @staticmethod
    def close_owner(self):
        self.owner.delete()

    @classmethod
    def close_element_sub(cls, owner, observer):
        instance = cls(owner, observer)
        instance.on_right_click = cls.close_owner
        instance.on_left_click = cls.close_owner
        return instance

    def __init__(self, owner, observer):
        self.owner = owner
        self.observer = observer
        self.ref = weakref.ref(self)
        self.observer.add_member(self.ref)

    def unsubscribe(self):
        self.observer.remove_member(self.ref)

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass
