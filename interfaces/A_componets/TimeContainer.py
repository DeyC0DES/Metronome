import asyncio
import pygame

from flet import *

class TimeContainer(UserControl):
    def __init__(self, number, time):
        super().__init__()
        # pygame initializing
        pygame.init()
        pygame.mixer.init()

        # audio
        self.downbeat = pygame.mixer.Sound('C:\\Users\\toxic\\OneDrive\\Desktop\\programs\\Softwares\\Metronome\\audios\\downbeat.mp3')
        self.upbeat = pygame.mixer.Sound('C:\\Users\\toxic\\OneDrive\\Desktop\\programs\\Softwares\\Metronome\\audios\\upbeat.mp3')

        self.text = number
        self.time = time
        self.container = Container()

    def update_time(self, time):
        self.time = time
        self.container.animate = animation.Animation(int(self.time * 1000), AnimationCurve.EASE_IN_OUT)
        self.container.update()
        self.update()

    async def blink(self):
        self.container.bgcolor = '#fa8128' if self.text != '1' else '#b0f2c2'
        self.container.content.controls[0].color = 'black'
        self.update()

        # tick sound
        match self.text:
            case '1':
                self.downbeat.play()
            case _:
                self.upbeat.play()

        await asyncio.sleep(self.time)
        self.container.bgcolor = '#131313'
        self.container.content.controls[0].color = '#fa8128' if self.text != '1' else '#b0f2c2'
        self.update()

    def build(self):

        self.container = Container(
            width=40,
            height=40,
            bgcolor='#131313',
            border_radius=100,
            border=border.all(0.5, '#fa8128'),
            padding=padding.only(top=8),
            animate=animation.Animation(self.time * 1000, AnimationCurve.EASE_IN_OUT),
            alignment=alignment.center,
            content=Column(
                controls=[
                    Text(
                        self.text,
                        color='#fa8128',
                        weight=FontWeight.BOLD
                    )
                ]
            )
        )

        if self.text == '1':
            self.container.border = border.all(0.5, '#b0f2c2')
            self.container.content.controls[0].color = '#b0f2c2'

        return self.container