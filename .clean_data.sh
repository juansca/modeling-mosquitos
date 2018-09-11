#!/bin/bash
INSTANCES=2
OVERLAPPING=0.5

# MAIN ----------------------------------------------------------------------

rm data/* -f
rm instances/* -f

# Instances for tunning
python data/clean_data.py -i data/raw_data/clorinda.csv -o tunning/instances/ --instances $INSTANCES --overlap $OVERLAPPING
python data/clean_data.py -i data/raw_data/pampa.csv -o tunning/instances/ --instances $INSTANCES --overlap $OVERLAPPING
python data/clean_data.py -i data/raw_data/iguazu.csv -o tunning/instances/ --instances $INSTANCES --overlap $OVERLAPPING

# Cleaned data to train and eval models
python data/clean_data.py -i data/raw_data/tartagal.csv -o data/cleaned_data/tartagal/
python data/clean_data.py -i data/raw_data/clorinda.csv -o data/cleaned_data/clorinda/
python data/clean_data.py -i data/raw_data/pampa.csv -o data/cleaned_data/pampa/
python data/clean_data.py -i data/raw_data/iguazu.csv -o data/cleaned_data/iguazu/

# Trap ctrl-c and other exit signals and delete all temporary files
trap TrapError 1 2 3 15;
function TrapError() {
    echo "Saliendo...";
    rm data/* -f
    rm instances/* -f
    exit;
}
