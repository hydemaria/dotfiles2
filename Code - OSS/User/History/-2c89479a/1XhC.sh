#!/bin/bash

# Define as opções do menu
opcoes="Desligar\nReiniciar"

# Abre o menu e guarda a escolha
escolha=$(echo -e "<span color='#503850'>Desligar</span>\n<span color='#503850'>Reiniciar</span>" | rofi -dmenu -p "Energia" -markup-rows)
# Verifica se algo foi escolhido. Se o usuário apertar Esc, ele sai sem fazer nada.
if [ -z "$escolha" ]; then
    exit 0
fi

# Executa a ação baseada na escolha
case "$escolha" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac