# Hybrid Load Balancer Demo Guide

This guide demonstrates the hybrid load balancing system in SkillNest using Docker.

## 🚀 Quick Start

### 1. Start the Load Balanced System

```bash
docker-compose -f docker-compose-loadbalancer.yml up -d
```

This will start:
- **PostgreSQL** (port 5432)
- **Redis** (port 6379)
- **Backend Instance 1** (port 8081)
- **Backend Instance 2** (port 8082)
- **Backend Instance 3** (port 8083)
- **Frontend** (port 3000)

### 2. Verify All Instances are Running

```bash
docker-compose -f docker-compose-loadbalancer.yml ps
```

### 3. Check Health of Each Instance

```bash
# Check instance 1
curl http://localhost:8081/api/health

# Check instance 2
curl http://localhost:8082/api/health

# Check instance 3
curl http://localhost:8083/api/health
```

Expected response:
```json
{
  "status": "UP",
  "service": "SkillNest Backend",
  "timestamp": 1713172800000
}
```

## 📊 Demo Scenarios

### Scenario 1: Round Robin Distribution

Submit multiple code submissions and observe which instance handles each request.

```bash
# Monitor backend logs in separate terminals
docker logs -f skillnest-backend-1
docker logs -f skillnest-backend-2
docker logs -f skillnest-backend-3
```

Then make a submission via the frontend or API. You'll see the load balancer distributing requests across instances using Round Robin.

### Scenario 2: Health Check & Failover

Simulate an instance failure and observe automatic failover:

```bash
# Stop backend-2
docker stop skillnest-backend-2

# Make a submission - it should automatically route to healthy instances (1 and 3)
```

Check the logs - you'll see:
- Health check marking instance 2 as unhealthy
- Requests being distributed to instances 1 and 3 only
- Automatic retry on failure

### Scenario 3: Instance Recovery

```bash
# Restart backend-2
docker start skillnest-backend-2

# Wait for health checks to refresh (2 minutes cache TTL)
# Or manually clear cache via Redis CLI
docker exec skillnest-redis redis-cli KEYS "loadbalancer:health:*"
docker exec skillnest-redis redis-cli DEL <cache-keys>

# Instance 2 will be marked healthy again and receive requests
```

### Scenario 4: Request Count Tracking

Monitor request distribution via Redis:

```bash
# Connect to Redis
docker exec -it skillnest-redis redis-cli

# Check request counts
KEYS loadbalancer:request_count:*
GET loadbalancer:request_count:http://backend-1:8080
GET loadbalancer:request_count:http://backend-2:8080
GET loadbalancer:request_count:http://backend-3:8080
```

### Scenario 5: Load-Aware Balancing (Optional)

Modify the load balancer to use the least-loaded instance instead of Round Robin:

In `HybridLoadBalancerService.java`, change the instance selection logic to use `getLeastLoadedInstance()`.

## 🧪 Testing the Load Balancer

### Test Script

Create a test script to submit multiple requests:

```bash
#!/bin/bash
for i in {1..10}; do
  echo "Submission $i"
  curl -X POST http://localhost:8081/api/submissions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_JWT_TOKEN" \
    -d '{
      "problemId": 1,
      "code": "print(\"Hello World\")",
      "language": "PYTHON"
    }'
  echo ""
  sleep 2
done
```

### Monitor Logs

```bash
# Watch all backend logs simultaneously
docker-compose -f docker-compose-loadbalancer.yml logs -f backend-1 backend-2 backend-3
```

Look for log entries like:
```
INFO: Attempt 1/3: Executing on instance http://backend-1:8080
INFO: Successfully executed on instance: http://backend-1:8080
```

## 🔧 Configuration

### Disable Load Balancer

To run without load balancing (single instance mode):

```bash
docker-compose -f docker-compose.yml up -d
```

Or set environment variable:
```bash
LOADBALANCER_ENABLED=false docker-compose -f docker-compose-loadbalancer.yml up
```

### Add More Instances

Edit `docker-compose-loadbalancer.yml` and add:

```yaml
backend-4:
  build:
    context: ./springboot-backend
    dockerfile: Dockerfile
  container_name: skillnest-backend-4
  environment:
    LOADBALANCER_ENABLED: "true"
    LOADBALANCER_INSTANCES_0: http://backend-1:8080
    LOADBALANCER_INSTANCES_1: http://backend-2:8080
    LOADBALANCER_INSTANCES_2: http://backend-3:8080
    LOADBALANCER_INSTANCES_3: http://backend-4:8080
  ports:
    - "8084:8080"
  # ... other config
```

## 📈 Performance Monitoring

### View Redis Metrics

```bash
docker exec skillnest-redis redis-cli INFO
```

### Check Docker Stats

```bash
docker stats skillnest-backend-1 skillnest-backend-2 skillnest-backend-3
```

## 🛑 Cleanup

```bash
# Stop all services
docker-compose -f docker-compose-loadbalancer.yml down

# Remove volumes (WARNING: deletes data)
docker-compose -f docker-compose-loadbalancer.yml down -v
```

## 🔍 Troubleshooting

### Instances Not Communicating

Check Docker network:
```bash
docker network inspect skillnest-network
```

### Health Check Failures

Verify health endpoint:
```bash
docker exec skillnest-backend-1 curl http://localhost:8080/api/health
```

### Redis Connection Issues

Test Redis connection:
```bash
docker exec skillnest-redis redis-cli ping
```

### Port Conflicts

If ports are already in use, modify the port mappings in `docker-compose-loadbalancer.yml`.

## 🎯 Key Features Demonstrated

1. **Round Robin Load Balancing** - Distributes requests across instances
2. **Health Check Integration** - Monitors instance health via `/api/health`
3. **Automatic Failover** - Routes around unhealthy instances
4. **Retry Mechanism** - Up to 2 retries before fallback
5. **Redis Caching** - Caches health status and request counts
6. **Graceful Degradation** - Falls back to local execution if all remote instances fail
7. **Zero Downtime** - Can add/remove instances dynamically

## 📝 Next Steps

- Integrate with Spring Cloud LoadBalancer for more advanced features
- Add circuit breaker pattern (Resilience4j)
- Implement weighted load balancing based on instance capacity
- Add metrics collection (Prometheus/Grafana)
- Implement service discovery (Eureka/Consul)
