#!/bin/bash

# Define as opções do menu
opcoes="Desligar\nReiniciar"

# Abre o menu e guarda a escolha
escolha=$(echo -e "$opcoes" | rofi -dmenu -p "Energia" -theme ~/.config/rofi/energia.rasi)
if [ -z "$escolha" ]; then
    exit 0
fi

# Executa a ação baseada na escolha
case "$escolha" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac