#!/bin/bash
killall waypaper
killall waybar

sleep 1

waypaper --restore &
waybar &
