# -*- coding: utf-8 -*-
# Copyright (c) 2014 Jim Kemp <kemp.jim@gmail.com>
# Copyright (c) 2017 Gene Liverman <gene@technicalissues.us>
# Distributed under the MIT License (https://opensource.org/licenses/MIT)

import datetime
import pygame

from piweatherrock.plugin_weather_common import PluginWeatherCommon


class PluginWeatherDaily:
    """
    This plugin is resposible for displaying the screen with the daily
    forecast.
    """

    def __init__(self, weather_rock):
        self.screen = None
        self.weather = None
        self.weather_common = None

    def get_rock_values(self, weather_rock):
        self.screen = weather_rock.screen
        self.weather = weather_rock.weather
        self.weather_common = PluginWeatherCommon(weather_rock)

    def disp_daily(self, weather_rock):
        self.get_rock_values(weather_rock)

        self.weather_common.disp_weather_top(weather_rock)

        # Today
        today = self.weather.daily[0]
        today_string = "Today"
        multiplier = 1
        self.weather_common.display_subwindow(today, today_string, multiplier)

        # counts from 0 to 2
        for future_day in range(3):
            this_day = self.weather.daily[future_day + 1]
            this_day_no = datetime.datetime.fromtimestamp(this_day.time)
            this_day_string = this_day_no.strftime("%A")
            multiplier += 2
            self.weather_common.display_subwindow(
                this_day, this_day_string, multiplier)

        # Update the display
        pygame.display.update()
