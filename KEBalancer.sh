#!/bin/sh
KE_EPT=0.0.0.0:5020
TEXT="What is the melting point of silver?"
echo "{\"text\":\"$TEXT\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js $KE_EPT
