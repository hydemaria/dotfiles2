#!/bin/bash

# Aqui definimos as cores para cada opção usando markup

# Abre o rofi usando o tema energia.rasi e habilitando o markup
escolha=$(echo -e "$opcoes" | rofi -dmenu -p "Energia" -markup-rows -theme ~/.config/rofi/energia.rasi)

# Remove as tags de formatação para que o sistema entenda o comando
limpo=$(echo "$escolha" | sed 's/<[^>]*>//g')

case "$limpo" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac