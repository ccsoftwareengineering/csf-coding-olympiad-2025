import pygame
import typing

if typing.TYPE_CHECKING:
    from structures.hud.input_box import InputBox
    from structures.game import Game


class InputHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        # Makes game ignore inputs put into an input box!
        self.selected_input_box: typing.Optional['InputBox'] = None

        self.key_on_down = {}
        self.key_down = set()
        self.key_on_up = {}

        self.mouse_on_down = {}
        self.mouse_down = set()
        self.mouse_on_up = {}

        self.mouse_focused = True

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
            if func is not None:
                func(value)

    def get_key_names_down(self):
        final = []
        for key in self.key_down:
            final.append(pygame.key.name(key))
        return final

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if self.selected_input_box is not None:
                self.selected_input_box.process_down(event)
                return
            qualifier = event.key not in self.key_down
            self.key_down.add(event.key)
            self.game.telemetry_handler.set_value('Keys Down', '+'.join(self.get_key_names_down()))
            # self.run_events('key_down', event.key)
            if qualifier:
                self.key_on_down[event.key] = True
                self.game.telemetry_handler.set_value('Key Down', pygame.key.name(event.key))
                self.run_events('key_on_down', event)
        elif event.type == pygame.KEYUP:
            if self.selected_input_box is not None:
                self.selected_input_box.process_up(event)
                return
            self.key_on_up[event.key] = True
            self.key_down.discard(event.key)
            self.game.telemetry_handler.set_value('Key Up', pygame.key.name(event.key))
            self.game.telemetry_handler.set_value('Keys Down', '+'.join(self.get_key_names_down()))
            self.run_events('key_on_up', event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down.add(event.button)
            self.run_events('mouse_down', event)
            if event.button not in self.mouse_down:
                self.mouse_on_down[event.button] = True
                self.run_events('mouse_on_down', event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_on_up[event.button] = True
            self.run_events('mouse_on_up', event)
            self.mouse_down.discard(event.button)

        elif event.type == pygame.ACTIVEEVENT:
            if event.state == pygame.APPMOUSEFOCUS:
                if event.gain == 1:
                    self.mouse_focused = True
                else:
                    self.mouse_focused = False
            self.run_events('active_event', event)
        elif event.type == pygame.MOUSEWHEEL:
            self.run_events('mouse_wheel', event)
        else:
            name = pygame.event.event_name(event.type)
            self.game.telemetry_handler.set_value('Event Name', name)
            events = self.event_dict_map.get(name)
            if events:
                for fn in events:
                    fn(events)

    def update(self):
        self.key_on_down = {}
        self.key_on_up = {}
        self.mouse_on_down = {}
        self.mouse_on_up = {}
        for key in self.key_down:
            self.run_events('key_down', key)
