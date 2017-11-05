#! /bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "brew installing protobuf..."
brew install protobuf

echo "compiling with protoc compiler..."
protoc --python_out=./ ./proto/site.proto
protoc --python_out=./ ./proto/lattice.proto
protoc --python_out=./ ./proto/simulation.proto
protoc --python_out=./ ./proto/enabled_collection.proto
protoc --python_out=./ ./proto/elementary_reaction.proto
protoc --python_out=./ ./proto/process.proto
protoc --python_out=./ ./proto/cell.proto

echo "Done!"