#!/bin/bash
# Generate embedding
echo "Preparing Brain before starting streamlit"
python prepare.py

# Start streamlit server
echo "Starting streamlit"
streamlit run docuwizard.py