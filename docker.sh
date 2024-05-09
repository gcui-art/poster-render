docker run \
  --rm \
  -p 3000:3000 \
  -e "CONCURRENT=10" \
  -e "TOKEN=SDHJK78AADS" \
  -d \
  ghcr.io/browserless/chromium