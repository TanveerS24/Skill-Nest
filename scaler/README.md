# SkillNest Auto-Scaler

A process-aware horizontal auto-scaler for the SkillNest competitive programming platform. This daemon automatically scales Spring Boot, FastAPI, and Docker Executor services based on real-time metrics including CPU usage, queue depth, latency, and Redis cache hit rates.

## Features

- **Metrics Collection**: Every 5 seconds, collects CPU %, memory MB, process count, queue depth, and p95 latency from all instances
- **Smart Scaling Policy**: 
  - Scale UP when CPU > 70% OR queue depth > 20 OR p95 latency > 500ms for 2 consecutive ticks
  - Scale DOWN when CPU < 30% AND queue depth < 5 for 5 consecutive ticks
- **Service Bounds**:
  - Spring Boot: 1-6 instances
  - FastAPI: 1-4 instances
  - Docker Executor: 1-10 instances
- **Cooldown Period**: 60-second cooldown after any scale event per service
- **Redis-Aware Scaling**: Reduces Spring Boot instances when cache hit rate > 80%
- **Rate-Limit Awareness**: Caps executor scaling based on active users (30 submissions/minute per user)
- **Instance Lifecycle**: Automatic container creation, Nginx config updates, and graceful draining on scale-down
- **Dashboard**: Real-time web UI at `/scaler` showing instance metrics, scale events, and manual controls
- **REST API**: JSON endpoint at `/scaler/status` for programmatic access

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Auto-Scaler Daemon                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Spring Boot  │  │   FastAPI    │  │   Executor   │      │
│  │   (1-6)      │  │   (1-4)      │  │   (1-10)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            ▼                                 │
│                    ┌──────────────┐                          │
│                    │   Nginx      │  ← Dynamic upstream      │
│                    │ Load Balancer│    config updates        │
│                    └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Redis      │  ← Cache hit rate        │
                    │   PostgreSQL │  ← Active users          │
                    └──────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Docker socket access for the scaler container
- Existing SkillNest services (Spring Boot, FastAPI, Executor)

### Installation

1. **Build and start with Docker Compose override**:

```bash
# Start base services
docker-compose up -d postgres redis backend ai-service frontend

# Start auto-scaler and Nginx
docker-compose -f docker-compose.override.yml up -d scaler nginx
```

2. **Access the dashboard**:

Open your browser to `http://localhost:9090/scaler` for the auto-scaler dashboard.

3. **Access the API**:

```bash
# Get current status
curl http://localhost:9090/scaler/status

# Manual scale up
curl -X POST http://localhost:9090/scaler/scale \
  -H "Content-Type: application/json" \
  -d '{"service": "springboot", "action": "scale_up"}'

# Freeze auto-scaling for a service
curl -X POST http://localhost:9090/scaler/scale \
  -H "Content-Type: application/json" \
  -d '{"service": "fastapi", "action": "freeze"}'
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://skillnest:skillnest@postgres:5432/skillnest` | PostgreSQL connection string |
| `REDIS_HOST` | `redis` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `JWT_SECRET` | `your-secret-key-change-in-production` | JWT secret for auth |

### Scaling Thresholds (in `scaler.py`)

```python
METRICS_INTERVAL = 5  # seconds between metric collection
SCALE_UP_THRESHOLD_CPU = 70  # percent
SCALE_UP_THRESHOLD_QUEUE = 20
SCALE_UP_THRESHOLD_LATENCY = 500  # ms
SCALE_DOWN_THRESHOLD_CPU = 30  # percent
SCALE_DOWN_THRESHOLD_QUEUE = 5
SCALE_UP_CONSECUTIVE_TICKS = 2
SCALE_DOWN_CONSECUTIVE_TICKS = 5
COOLDOWN_SECONDS = 60
DRAIN_TIMEOUT_SECONDS = 30
```

### Service Bounds (in `scaler.py`)

```python
SERVICE_BOUNDS = {
    "springboot": {"min": 1, "max": 6, "port": 8080, "image": "skillnest-backend:latest"},
    "fastapi": {"min": 1, "max": 4, "port": 8000, "image": "skillnest-ai-service:latest"},
    "executor": {"min": 1, "max": 10, "port": 9000, "image": "skillnest-executor:latest"},
}
```

## Dashboard Features

The dashboard provides:

- **Live Instance Cards**: Real-time CPU %, memory, process count, and queue depth for each instance
- **Overload Indicators**: Visual alerts when instances exceed thresholds
- **Scale Event Log**: History of all scale actions with reasons
- **Manual Controls**: Force scale up/down, freeze/unfreeze auto-scaling per service
- **Recommended Actions**: AI-recommended next actions based on current metrics
- **Cooldown Status**: Visual indication when services are in cooldown period
- **Redis Metrics**: Cache hit rate for Spring Boot service
- **Rate Limit Info**: Max submission RPS based on active users

## API Endpoints

### GET `/scaler`

Returns the dashboard HTML page.

### GET `/scaler/status`

Returns JSON with current system state:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "springboot": {
      "instance_count": 2,
      "instances": [
        {
          "container_id": "abc123...",
          "cpu_percent": 45.2,
          "memory_mb": 512.3,
          "process_count": 42,
          "queue_depth": 5,
          "p95_latency_ms": 120.5,
          "is_overloaded": false,
          "last_updated": "2024-01-15T10:30:00Z"
        }
      ],
      "last_scale_action": "scale_up",
      "last_scale_time": "2024-01-15T10:25:00Z",
      "cooldown_until": "2024-01-15T10:26:00Z",
      "is_frozen": false,
      "redis_cache_hit_rate": 85.5,
      "min_instances": 1,
      "max_instances": 6
    }
  },
  "scale_events": [...],
  "recommended_actions": {
    "springboot": "scale_down",
    "fastapi": "no_action",
    "executor": "scale_up"
  }
}
```

### POST `/scaler/scale`

Manual override for scaling actions.

**Request Body**:
```json
{
  "service": "springboot",
  "action": "scale_up"  // or "scale_down", "freeze", "unfreeze"
}
```

## How It Works

### Metrics Collection

1. Every 5 seconds, the scaler queries Docker for all containers labeled with `skillnest.service=<name>`
2. For each container, it collects:
   - CPU % from Docker Stats API
   - Memory MB from Docker Stats API
   - Process count from Docker Stats API
   - Queue depth and latency from service-specific endpoints:
     - Spring Boot: `/actuator/metrics/http.server.requests`
     - FastAPI: `/metrics` (Prometheus format)
     - Executor: Count of running executor containers
3. Redis metrics (cache hit rate) are collected for Spring Boot
4. Active user count is collected from Redis for rate-limit calculations

### Scaling Decision Logic

For each service:

1. **Check cooldown**: If service is in cooldown period, skip
2. **Check freeze**: If service is frozen, skip
3. **Calculate averages**: CPU, queue depth, and latency across all instances
4. **Apply Redis-aware logic**: If Spring Boot cache hit rate > 80%, bias toward scale-down
5. **Apply rate-limit logic**: If executor RPS exceeds `(active_users × 30) / 60`, cap scale-up
6. **Check thresholds**:
   - If CPU > 70% OR queue > 20 OR latency > 500ms: increment scale-up counter
   - If CPU < 30% AND queue < 5: increment scale-down counter
   - Otherwise: reset counters
7. **Execute action**:
   - If scale-up counter >= 2: Scale up (if below max)
   - If scale-down counter >= 5: Scale down (if above min)

### Instance Lifecycle

**Scale Up**:
1. Pull the correct Docker image
2. Inject environment variables (DB URL, Redis URL, JWT secret)
3. Create container with `skillnest.service=<name>` label
4. Update Nginx upstream config with new container IP
5. Reload Nginx with `nginx -s reload`
6. Set cooldown timer

**Scale Down**:
1. Select least-loaded instance
2. Remove from Nginx upstream config
3. Reload Nginx
4. Drain instance (stop new requests, wait up to 30s for in-flight requests)
5. Stop and remove container
6. Set cooldown timer

## Troubleshooting

### Scaler not starting

- Check Docker socket is mounted: `/var/run/docker.sock:/var/run/docker.sock`
- Verify network connectivity to Redis and PostgreSQL
- Check logs: `docker logs skillnest-scaler`

### Instances not scaling

- Check if service is frozen (dashboard shows ❄️)
- Check if in cooldown period
- Verify metrics are being collected (check dashboard)
- Check service bounds (min/max instances)

### Nginx not updating

- Verify Nginx config directory is mounted: `./nginx:/etc/nginx/conf.d`
- Check scaler has write permissions to config directory
- Test Nginx reload manually: `docker exec skillnest-nginx nginx -s reload`

### Metrics not collecting

- Verify service containers have `skillnest.service=<name>` label
- Check Spring Boot Actuator is enabled: `/actuator/metrics` endpoint
- Check FastAPI metrics endpoint: `/metrics`
- Check network connectivity between scaler and service containers

## Development

### Running locally (without Docker)

```bash
# Install dependencies
cd scaler
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://skillnest:skillnest@localhost:5432/skillnest"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"

# Run scaler
python scaler.py
```

### Adding new services

1. Add service bounds to `SERVICE_BOUNDS` in `scaler.py`
2. Implement service-specific metrics collection in `_collect_<service>_metrics()`
3. Add Nginx upstream config template
4. Update dashboard to display new service

## Monitoring

The scaler uses `structlog` for structured logging. Logs are output in JSON format:

```json
{
  "event": "Scaling up service",
  "service": "springboot",
  "current": 2,
  "reason": "High load: CPU 75.5%, Queue 25.0, Latency 550.0ms",
  "level": "info",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

View logs:
```bash
docker logs -f skillnest-scaler
```

## Security Considerations

- The scaler requires Docker socket access - ensure it runs in a trusted environment
- JWT secret should be set via environment variable in production
- Dashboard is currently unauthenticated - add authentication for production
- Nginx configs are written by the scaler - ensure proper file permissions

## License

Part of the SkillNest project. See main LICENSE file for details.
