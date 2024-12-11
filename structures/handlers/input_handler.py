import pygame


class InputHandler:
    def __init__(self, game):
        self.game = game
        self.selected_input_box = None

        self.key_on_down = {}
        self.key_down = set()
        self.key_on_up = {}

        self.mouse_on_down = {}
        self.mouse_down = set()
        self.mouse_on_up = {}

        self.event_dict_map = {
            # 'key_on_down': {},
            # 'key_down': {},
            # 'key_on_up': {},
            # 'mouse_on_down': {},
            # 'mouse_down': {},
            # 'mouse_on_up': {},
        }

    def is_key_down(self, key):
        return key in self.key_down

    def subscribe(self, event, function, event_id="default"):
        if event not in self.event_dict_map:
            self.event_dict_map[event] = {}
        self.event_dict_map[event][event_id] = function

    def unsubscribe(self, event, event_id="default"):
        self.event_dict_map[event][event_id] = None

    def run_events(self, event, value):
        event = self.event_dict_map.get(event)
        if not event:
            return
        for func in event.values():
            func(value)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key not in self.key_down:
                self.key_on_down[event.key] = True
                self.run_events('key_on_down', event.key)
            self.key_down.add(event.key)
            self.run_events('key_down', event.key)
        elif event.type == pygame.KEYUP:
            self.key_on_up[event.key] = True
            self.run_events('key_on_up', event.key)
            self.key_down.discard(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button not in self.mouse_down:
                self.mouse_on_down[event.button] = True
                self.run_events('mouse_on_down', event.button)
            self.mouse_down.add(event.button)
            self.run_events('mouse_down', event.button)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_on_up[event.button] = True
            self.run_events('mouse_on_up', event.button)
            self.mouse_down.discard(event.button)

    def update(self):
        self.key_on_down = {}
        self.key_on_up = {}
        self.mouse_on_down = {}
        self.mouse_on_up = {}
