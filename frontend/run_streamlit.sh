#!/bin/bash
export PATH="/root/.venv/bin:$PATH"
exec /root/.venv/bin/streamlit run /app/streamlit_app/app.py \
  --server.port 3000 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.enableStaticServing true \
  --browser.gatherUsageStats false

