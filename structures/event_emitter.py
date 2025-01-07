all_id = 0


class EventEmitter:

    def __init__(self):
        global all_id
        self.events = {}
        self.id = all_id
        all_id += 1

    def on(self, event, function, event_id="default"):
        if event not in self.events:
            self.events[event] = {}
        self.events[event][event_id] = function

    def off(self, event, event_id="default"):
        self.events[event][event_id] = None

    def emit(self, event, value):
        print(f'emitting: {event} ({self.id})')
        event = self.events.get(event)
        if not event:
            return
        for func in event.values():
            if func is not None:
                func(value)
