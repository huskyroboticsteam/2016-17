#!/usr/bin/env python

# -*- coding: utf-8 -*-

import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.label import Label

# Hello World example by programmatically creating widgets

class HelloWorldApp(App):
    def build(self):
        # Documentation for the Label class: https://kivy.org/docs/api-kivy.uix.label.html
        # See https://kivy.org/docs/api-kivy.metrics.html for the acceptable units of font_size
        return Label(text="Hello World", font_size="50sp")

if __name__ == '__main__':
    HelloWorldApp().run()
