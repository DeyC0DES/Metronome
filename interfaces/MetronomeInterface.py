import asyncio

from flet import *

from interfaces.A_componets.TimeContainer import TimeContainer
from interfaces.utils.BeatsCalc import BeatsCalc

class MetronomeInterface(UserControl):
    def __init__(self):
        super().__init__()
        # presets
        self.bpm = 60
        self.bps = 1
        self.time = 1

        # run statement
        self.running = False

    def build(self):

        def handle_update_time():
            _time1.update_time(self.time)
            _time2.update_time(self.time)
            _time3.update_time(self.time)
            _time4.update_time(self.time)

        def handle_bpm_change(e):

            def validate_numeric_input(event):
                if not event.control.value.isdigit():
                    event.control.value = ''.join(filter(str.isdigit, event.control.value))
                    event.control.update()

            validate_numeric_input(e)
            beat_calc = BeatsCalc()

            if _bpm_textfield.value == '' or _bpm_textfield.value == '0':
                self.bpm = 1
            else:
                try:
                    self.bpm = int(_bpm_textfield.value)
                except Exception:
                    return


            self.bps = beat_calc.calcBps(self.bpm)
            self.time = beat_calc.calcSleepTime(self.bps)

            handle_update_time()

        def handler_click(func):
            async def reset_time():
                await asyncio.gather(
                    _time1.blink(),
                    _time2.blink(),
                    _time3.blink(),
                    _time4.blink()
                )

            def stop():
                self.running = False

            async def start():
                self.running = True
                while self.running:
                    await _time1.blink()
                    await _time2.blink()
                    await _time3.blink()
                    await _time4.blink()
                self.page.run_task(reset_time)

            match func:
                case 'stop':
                    stop()
                    _play_button.content.controls[0].name = Icons.PLAY_ARROW_ROUNDED
                    _play_button.update()
                    _play_button.on_click = lambda e: handler_click('start')
                case 'start':
                    self.page.run_task(start)
                    _play_button.content.controls[0].name = Icons.PAUSE_ROUNDED
                    _play_button.update()
                    _play_button.on_click = lambda e: handler_click('stop')

            self.page.update()

        # A components
        _time1 = TimeContainer('1', self.time)
        _time2 = TimeContainer('2', self.time)
        _time3 = TimeContainer('3', self.time)
        _time4 = TimeContainer('4', self.time)

        # B components
        _bpm_textfield = TextField(
            value=self.bpm,
            text_size=25,
            text_align=TextAlign.CENTER,
            color='#666666',
            width=140,
            border_width=0,
            border=None,
            content_padding=padding.only(top=0),
            max_length=3,
            on_change= lambda e: handle_bpm_change(e)
        )

        _play_button = ElevatedButton(
            width=170,
            height=40,
            style=ButtonStyle(
                bgcolor='#fa8128',
                shape=RoundedRectangleBorder(radius=10)
            ),
            on_click=lambda e: handler_click('start'),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=Icons.PLAY_ARROW_ROUNDED,
                        color='white',
                        size=25
                    )
                ]
            )
        )

        # main
        _main_container = Container(
            width=320,
            height=440,
            bgcolor='#131313',
            content=Stack(
                controls=[
                    Column(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Column(
                                alignment=MainAxisAlignment.END,
                                controls=[
                                    # time
                                    Container(
                                        width=320,
                                        height=100,
                                        alignment=alignment.center,
                                        content=Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Row(
                                                    alignment=MainAxisAlignment.CENTER,
                                                    spacing=20,
                                                    controls=[
                                                        _time1,
                                                        _time2,
                                                        _time3,
                                                        _time4
                                                    ]
                                                ),
                                            ]
                                        )
                                    ),

                                    # bpm container
                                    Row(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            Container(
                                                width=220,
                                                height=40,
                                                border_radius=10,
                                                border=border.all(0.5, '#fa8128'),
                                                content=Row(
                                                    alignment=MainAxisAlignment.START,
                                                    spacing=0,
                                                    controls=[
                                                        Container(
                                                            width=80,
                                                            height=40,
                                                            bgcolor='#fa8128',
                                                            border_radius=border_radius.only(top_left=10, bottom_left=10),
                                                            content=Row(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Text(
                                                                        'bpm',
                                                                        weight=FontWeight.BOLD,
                                                                        size=25,
                                                                        color='#131313'
                                                                    )
                                                                ]
                                                            )
                                                        ),

                                                        # text field
                                                        Container(
                                                            width=200,
                                                            height=40,
                                                            content=Column(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Row(
                                                                        expand=True,
                                                                        alignment=MainAxisAlignment.START,
                                                                        controls=[
                                                                            _bpm_textfield
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ]
                            ),

                            Column(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Row(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            Container(
                                                width=320,
                                                height=100,
                                                content=Row(
                                                    alignment=MainAxisAlignment.CENTER,
                                                    controls=[
                                                        _play_button
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        return _main_container