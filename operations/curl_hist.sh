curl -N -X POST "http://127.0.0.1:8001/chat/stream" \
-H "Content-Type: application/json" \
-H "x-api-key: bHlG973WDZRp4Zw" \
-d '{
  "prompt": "E quem foi o presidente na época da sua inauguração?",
  "history": [
    {
      "role": "user",
      "text": "Qual a capital do Brasil e qual sua principal característica arquitetônica?"
    },
    {
      "role": "model",
      "text": "A capital do Brasil é Brasília. Sua principal característica arquitetônica é o modernismo, com um plano piloto em formato de avião projetado por Lúcio Costa e edifícios icônicos criados por Oscar Niemeyer."
    }
  ]
}'