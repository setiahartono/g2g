#!/bin/bash
set -euo pipefail

echo "==> Checking prerequisites..."

command -v docker >/dev/null || {
    echo "Docker is not installed."
    exit 1
}

docker info >/dev/null 2>&1 || {
    echo "Docker Desktop is not running."
    exit 1
}

command -v zip >/dev/null || {
    echo "zip is not installed."
    exit 1
}

[ -f requirements.txt ] || {
    echo "requirements.txt not found."
    exit 1
}

[ -d src ] || {
    echo "src/ directory not found."
    exit 1
}

echo "==> Preparing build directory..."
rm -rf build deployment.zip
mkdir -p build

echo "==> Installing dependencies for Lambda (Python 3.12, x86_64)..."

docker run --platform linux/amd64 --rm \
    --entrypoint /bin/bash \
    -v "$PWD":/var/task \
    -w /var/task \
    public.ecr.aws/lambda/python:3.12 \
    -c "python -m pip install -r requirements.txt -t build/"

echo "==> Copying application source..."
cp -r src build/

echo "==> Creating deployment package..."
cd build
zip -qr ../deployment.zip .
cd ..

echo "==> Deployment package created successfully!"
echo "File: $(pwd)/deployment.zip"
echo "Size: $(du -h deployment.zip | cut -f1)"
