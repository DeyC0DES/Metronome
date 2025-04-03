from flet import *

from interfaces.MetronomeInterface import MetronomeInterface


def start(page: Page):

    def change_route(route):

        def column_presets(interface):
            _main_column.controls.clear()
            _main_column.controls.append(interface)

        def add_view(interface, path):
            column_presets(interface)
            page.views.append(
                View(
                    path,
                    padding=0,
                    controls=[
                        _main_column
                    ]
                )
            )
            page.update()

        if _main_column.controls not in page.controls:
            page.add(_main_column)

        match page.route:
            case 'metronome':
                add_view(metronome_interface, 'metronome')

    # page config
    page.window.width = 320
    page.window.height = 480
    page.title = 'Metronome'
    page.window.resizable = False
    page.padding = 0
    page.window.always_on_top = True

    # interfaces
    metronome_interface = MetronomeInterface()

    # main things
    _main_column = Stack(
        controls=[

        ]
    )

    page.on_route_change = change_route
    page.go('metronome')
    page.update()

if __name__ == '__main__':
    app(target=start)