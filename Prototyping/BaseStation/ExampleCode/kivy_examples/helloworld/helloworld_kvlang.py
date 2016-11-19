#!/usr/bin/env python

# -*- coding: utf-8 -*-

import kivy
kivy.require("1.9.1")

from kivy.app import App

# Hello World example by using the KV language
# Documentation for the KV language: https://kivy.org/docs/guide/lang.html

class HelloWorldKvApp(App):
    # No code needed here; it is constructed from the KV language file helloworldkv.kv
    pass

if __name__ == '__main__':
    HelloWorldKvApp().run()
