#!/bin/bash

# Démarrer le serveur Ollama en arrière-plan
echo "Starting Ollama server..."
ollama serve &

# Attendre un peu que le serveur démarre (tu peux ajuster le temps ou tester mieux)
sleep 10s

# Installer les composants nécessaires
to_install="gemma3"

for hey in $to_install
do
    echo "Installing $hey..."
    if ! ollama pull $hey; then
        echo "Failed to install $hey"
        exit 1
    fi
done
