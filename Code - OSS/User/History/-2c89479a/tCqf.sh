#!/bin/bash

# Abre o rofi usando o arquivo base, mas aplicando as cores específicas via linha de comando
escolha=$(echo -e "Desligar\nReiniciar" | rofi -dmenu -p "Energia" \
    -theme ~/.config/rofi/energia.rasi \
    -theme-str 'element-text { text-color: #503850; }')

case "$escolha" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac