# Intelligent Ticket Intake Service — System Design

## 1. Problem & Goal
Manual support ticket triage is slow and error-prone. This service automates ticket intake by enriching incoming complaints with geographic context, classifying urgency and sentiment via an LLM, and storing structured records in PostgreSQL.

## 2. System Flow
```text
Client (POST /tickets)
   │
   ▼
[FastAPI Route] ──▶ Validates JSON payload
   │
   ▼
[Service Layer] ──▶ 1. Calls ip-api.com (Location & Timezone)
   │                2. Calls LLM API (Urgency, Sentiment, Summary)
   │                3. Saves enriched record to PostgreSQL
   ▼
Client ◀── Returns structured JSON response (HTTP 201)
```

## 3. API Contract

### Request (`POST /tickets`)
```json
{
  "ticket_text": "My payment failed twice and my account is locked!",
  "ip_address": "103.21.244.0"
}
```

### Response (`201 Created`)
```json
{
  "ticket_id": 101,
  "country": "India",
  "timezone": "Asia/Kolkata",
  "urgency": "HIGH",
  "sentiment": "ANGRY",
  "summary": "Customer experienced two failed payments resulting in a locked account."
}
```

## 4. External Enrichment & Failure Strategy
- **API Choice:** `ip-api.com` (JSON endpoint, free tier, no API key required).
- **Rate Limit & Constraints:** Capped at **45 requests/minute** (returns HTTP `429` if exceeded) and uses HTTP.
- **Graceful Degradation:** If `ip-api.com` times out (>2 seconds) or rate-limits our server, the system will **not** fail the user's request. It will log a warning, default `country` and `timezone` to `"Unknown"`, and still complete the AI classification and database save.
