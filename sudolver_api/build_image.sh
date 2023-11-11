#!/bin/bash
set -euo pipefail
docker image build --progress=plain -t sudolver --build-arg BUILDKIT_INLINE_CACHE=1 .