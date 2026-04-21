# Langfuse Tracing Integration Guide

This observability lab now includes **Langfuse tracing** following best practices from the Langfuse Skills framework.

## What's Included

### 1. Langfuse Tracing Module (`app/langfuse_tracing.py`)
Provides utilities for tracing with Langfuse:
- **`get_langfuse_client()`** - Singleton client access
- **`set_trace_attributes()`** - Propagate trace context to all child observations
- **`trace_function()`** - Decorator for custom tracing
- **`flush_langfuse()`** - Ensure all traces are sent before shutdown

### 2. Chat Endpoint Instrumentation
The `/chat` endpoint now includes:
- **Root trace**: Named `"chat-request"` using `@observe` decorator
- **Trace attributes**: user_id_hash, session_id, feature, model, env
- **Nested span**: `"agent-execution"` with input/output tracking
- **PII masking**: Sensitive data scrubbed before logging

### 3. Lifecycle Management
- **Startup**: Initializes Langfuse client and verifies authentication
- **Shutdown**: Flushes all pending traces to ensure no data loss

## Configuration

### Prerequisites
1. Create a Langfuse account (free) at [cloud.langfuse.com](https://cloud.langfuse.com)
2. Get your API keys from **Settings > API Keys**
3. Update `.env` file with your credentials:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-your-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-key-here
LANGFUSE_HOST=https://cloud.langfuse.com  # or https://us.cloud.langfuse.com
```

### Current Setup
Credentials are configured in `.env` (demo keys provided for testing).

## Best Practices Implemented

### ✓ Baseline Requirements
- **Model name**: Captured from `LLM_MODEL` environment variable
- **Token usage**: Tracked through the tracing system
- **Descriptive names**: Traces use meaningful names (`chat-request`, `agent-execution`)
- **Span hierarchy**: Root trace with nested child spans for operations
- **Observation types**: Correctly typed as spans for non-LLM operations
- **Sensitive data**: PII redacted using `summarize_text()` scrubbing
- **Input/output**: Explicitly set on observations (not all function args)

### ✓ Context Enrichment
All traces include:
- `user_id_hash`: SHA256 hash for privacy-preserving user tracking
- `session_id`: Groups related messages for conversation analysis
- `feature`: Tags for per-feature performance analysis
- `model`: LLM model identification
- `env`: Environment (dev/staging/prod)

### ✓ Error Handling
- Graceful initialization with auth check
- Langfuse errors don't break the application
- Automatic trace flushing on shutdown

## Usage

### View Traces
1. Start the application:
```bash
python -m uvicorn app.main:app --reload
```

2. Send a request:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u_demo_001",
    "session_id": "s_demo_001",
    "feature": "qa",
    "message": "What is observability?"
  }'
```

3. View traces in Langfuse dashboard:
   - Go to [cloud.langfuse.com](https://cloud.langfuse.com)
   - View the "Traces" section
   - Click on individual traces to see hierarchy and attributes

### Trace Structure
```
chat-request (root trace)
├─ Input: User message (scrubbed)
├─ Attributes:
│  ├─ user_id: <hashed>
│  ├─ session_id: s_demo_001
│  ├─ tags: [feature:qa, model:gpt-4, env:dev]
│  └─ ...
└─ agent-execution (nested span)
   ├─ Input: Message + feature
   └─ Output: Answer + quality score
```

## Integration with Other Components

### Middleware (correlation_id)
- FastAPI middleware adds `correlation_id` to all requests
- Traces can be correlated with request logs

### Logging (structlog)
- Context variables (user_id_hash, session_id, etc.) enriched logs
- Structlog processors scrub PII before writing to JSONL
- Langfuse provides complementary distributed tracing view

### Metrics
- Latency, token usage, costs tracked in traces
- Can be queried via Langfuse dashboard

## Common Workflows

### Debug a Slow Response
1. Filter traces by `feature` in Langfuse dashboard
2. Sort by latency to find slow traces
3. Expand trace hierarchy to identify bottleneck span
4. Compare across users/sessions

### Analyze Feature Performance
1. Create dashboard filtered by `feature:qa` tag
2. Compare quality_score across user segments
3. Identify problematic user_id hashes

### Trace User Sessions
1. Filter by `session_id` in dashboard
2. See full conversation flow
3. Identify at which turn quality degraded

## Reference

- [Langfuse Documentation](https://langfuse.com/docs)
- [Python SDK Reference](https://python.reference.langfuse.com/)
- [Tracing Concepts](https://langfuse.com/docs/observability/data-model)
- [Score & Evaluation](https://langfuse.com/docs/scores/overview)

## Next Steps

1. ✓ Install Langfuse tracing (DONE)
2. Add custom scores for quality evaluation
3. Create Langfuse dashboards for monitoring
4. Integrate with alerts/SLOs
5. Use Langfuse prompt management for multi-version testing
