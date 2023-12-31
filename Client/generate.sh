docker run --rm \
  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
  -i /local/openapi.yaml \
  -g python \
  -o /local/out/python

rm -r ./openapi_client
cp -r ./out/python/openapi_client ./openapi_client

