#!/bin/bash

: ${1?"Usage: $0 Module_name"}
: ${2?"Usage: $0 filename"}

echo "export {default as $1} from './$2'"
