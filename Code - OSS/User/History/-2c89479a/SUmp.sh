#!/bin/bash

opcoes="Desligar\nReiniciar"
escolha=$(echo -e "$opcoes" | rofi -dmenu -p "Energia" -theme ~/.config/rofi/energia.rasi)

case "$escolha" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac