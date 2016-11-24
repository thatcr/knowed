class Descriptor(property):
    def __repr__(self):
        return self.fget.__code__.co_name
