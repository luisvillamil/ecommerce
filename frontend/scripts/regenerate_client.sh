#!/bin/bash

# Config variables
WORKING_DIR="src/client"
MODIFY_OPENAPI="scripts/modify-openapi-operationids.js"

# remove existing client directory if it exists
echo "removing $WORKING_DIR"
if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi

# pull new open api data. NOTE: backend must be running
echo pulling openai config
curl http://127.0.0.1:8000/api/v1/openapi.json > openapi.json
if [ $? -ne 0 ]; then
    rm openapi.json
    echo "curl failed. Exit the script"
    exit 1
fi

bun run $MODIFY_OPENAPI
if [ $? -ne 0 ]; then
    echo "$MODIFY_OPENAPI failed. Exit the script"
    exit 1
fi

# call regenerate client script using bun
echo regenerating client
bun run generate-client
if [ $? -ne 0 ]; then
    echo "generate-client failed. Exit the script"
    exit 1
fi

# cleanup directory
echo removing openapi.json
rm openapi.json
