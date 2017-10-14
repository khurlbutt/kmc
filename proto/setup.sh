#! /bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "brew installing protobuf..."
brew install protobuf

echo "compiling with protoc compiler..."
protoc --python_out=./ ./proto/site.proto
protoc --python_out=./ ./proto/lattice.proto

echo "Done!"