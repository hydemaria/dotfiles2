#!/bin/bash

# Aplicamos a classe ao elemento usando uma div ou span com class
opcoes="<element class='desligar'>Desligar</element>\n<element class='reiniciar'>Reiniciar</element>"

# O -markup-rows permite que o Rofi entenda a estrutura
escolha=$(echo -e "$opcoes" | rofi -dmenu -p "Energia" -markup-rows -theme ~/.config/rofi/energia.rasi)

# Limpa o texto para o comando
limpo=$(echo "$escolha" | sed 's/<[^>]*>//g')

case "$limpo" in
    "Desligar") poweroff ;;
    "Reiniciar") reboot ;;
esac