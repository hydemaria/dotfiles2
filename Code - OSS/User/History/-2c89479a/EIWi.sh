#!/bin/bash

# Define as opções do menu
opcoes="Desligar\nReiniciar"

# Abre o menu e guarda a escolha
escolha=$(echo -e "<span color='#503850'>Desligar</span>\n<span color='#503850'>Reiniciar</span>" | rofi -dmenu -p "Energia" \
    -markup-rows \
    -theme-str 'window {background-color: #1e1e2ecc;} \
                element selected {background-color: #ffb6c1; text-color: #1e1e2e;}')
if [ -z "$escolha" ]; then
    exit 0
fi

# Executa a ação baseada na escolha
case "$escolha" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac