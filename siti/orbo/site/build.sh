#!/bin/sh
# Crea index.html (pagina completa per GitHub Pages) da page.html.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  sed -n '1,/^<style>/p' page.html | sed '$d'
  printf '</head>\n<body>\n'
  sed -n '/^<style>/,$p' page.html
  printf '</body>\n</html>\n'
} > index.html
