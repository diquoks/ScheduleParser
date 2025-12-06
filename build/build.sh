# shellcheck disable=SC2046
poetry add $(cat "../requirements.txt")

rm -rf ../dist

poetry build