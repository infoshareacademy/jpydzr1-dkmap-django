#!/bin/bash
python -Wa ./TicTacToe/manage.py test --parallel --noinput --debug-sql --debug-mode --tag=enabled tests