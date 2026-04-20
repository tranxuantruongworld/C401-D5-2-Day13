# Day 13 Lab: Demo Script & Lead Guide

This guide is for **Member F (Demo Lead)** to orchestrate the 5-minute live demonstration.

## Demo Flow (5 Minutes Total)

### 1. Introduction (30s)
- **Objective**: Briefly state the goal of the lab.
- **Script**: "Hello everyone! Our team (D5-2) has instrumented a FastAPI agent with full observability. We're going to show you how we track requests from the user's click all the way to the database and back, even when things go wrong."

### 2. Normal Operation: The "Golden Path" (1m)
- **Action**: Run a simple request using `scripts/load_test.py`.
- **Show**: 
    - **Logs**: Show the JSON logs in terminal. Highlight the `correlation_id` and `user_id_hash` (PII Scrubbing).
    - **Traces**: Open Langfuse. Show a successful trace waterfall. Point out the `rag_lookup` and `llm_generation` spans.
- **Key Message**: "Every request is uniquely ID'd. Notice how the user's real email is never logged—we only store a hash."

### 3. Monitoring: The Dashboard (1m)
- **Action**: Open the 6-panel dashboard.
- **Show**:
    - Latency (P95), Error Rate, Cost, and Request Count.
    - Point out the SLO lines (e.g., Latency < 3000ms).
- **Key Message**: "This is our 'health at a glance'. We've set targets to ensure our users stay happy and our costs stay low."

### 4. Incident Response: "When it breaks" (2m)
- **Action**: Inject an incident (e.g., `python scripts/inject_incident.py --scenario rag_slow`).
- **Show**:
    - **Alerts**: Show the alert firing in terminal or log.
    - **Dashboard**: Show the latency spike or error rate jump.
    - **Traces**: Find the specific trace for the slow request. Show the `rag_lookup` taking 5+ seconds.
    - **Root Cause**: "The trace proves the RAG system is the bottleneck. The logs show the backend is waiting on a response."
- **Action**: Fix it by disabling the incident.

### 5. Conclusion (30s)
- **Script**: "By combining Logs for detail, Traces for flow, and Metrics for scale, we can identify and fix issues in minutes, not hours. Thank you!"

---

## Pro-Tips for the Lead:
- **Environment**: Have your browser tabs (Langfuse, Dashboard) and terminal windows pre-arranged.
- **Coordination**: Call on specific team members to explain their parts (e.g., "Trường, explain how you handled the PII scrubbing").
- **Recovery**: If the app crashes, stay calm. Use the logs to debug it live—that's the whole point of the lab!
