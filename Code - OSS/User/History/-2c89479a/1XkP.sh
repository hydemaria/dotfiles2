#!/bin/bash

# Define as opções com cores fixas (estilo markup)
opcoes="<span color='#503850'>Desligar</span>\n<span color='#503850'>Reiniciar</span>"

# Abre o rofi usando o tema específico para este menu
escolha=$(echo -e "$opcoes" | rofi -dmenu -p "Energia" \
    -markup-rows \
    -theme-str 'window {background-color: #1e1e2ecc; border: 2px; border-color: #ffb6c1;} \
                element.0 {background-color: #ff8e9e;} \
                element.1 {background-color: #ffd6dc;} \
                element selected {background-color: #ffb6c1; text-color: #1e1e2e;}')

# Remove as tags de cor para processar o comando puro
limpo=$(echo "$escolha" | sed 's/<[^>]*>//g')

# Executa a ação baseada na escolha
case "$limpo" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac