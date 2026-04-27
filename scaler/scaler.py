#!/usr/bin/env python3
"""
SkillNest Auto-Scaler Daemon
Process-aware horizontal auto-scaler for Spring Boot, FastAPI, and Docker Executor services
"""

import structlog
import time
import threading
import signal
import sys
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import docker
import requests
import redis
from flask import Flask, jsonify, request, render_template
from jinja2 import Template

# Configuration
METRICS_INTERVAL = 5  # seconds
SCALE_UP_THRESHOLD_CPU = 70  # percent
SCALE_UP_THRESHOLD_QUEUE = 20
SCALE_UP_THRESHOLD_LATENCY = 500  # ms
SCALE_DOWN_THRESHOLD_CPU = 30  # percent
SCALE_DOWN_THRESHOLD_QUEUE = 5
SCALE_UP_CONSECUTIVE_TICKS = 2
SCALE_DOWN_CONSECUTIVE_TICKS = 5
COOLDOWN_SECONDS = 60
DRAIN_TIMEOUT_SECONDS = 30

# Service bounds
SERVICE_BOUNDS = {
    "springboot": {"min": 1, "max": 6, "port": 8080, "image": "skillnest-backend:latest"},
    "fastapi": {"min": 1, "max": 4, "port": 8000, "image": "skillnest-ai-service:latest"},
    "executor": {"min": 1, "max": 10, "port": 9000, "image": "skillnest-executor:latest"},
}

# Environment variables
DB_URL = os.getenv("DATABASE_URL", "postgresql://skillnest:skillnest@postgres:5432/skillnest")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")

# Setup logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
log = structlog.get_logger()


class ScaleAction(Enum):
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    NO_ACTION = "no_action"
    FROZEN = "frozen"


@dataclass
class InstanceMetrics:
    container_id: str
    cpu_percent: float
    memory_mb: float
    process_count: int
    queue_depth: int
    p95_latency_ms: float
    is_overloaded: bool
    last_updated: datetime


@dataclass
class ServiceState:
    name: str
    instances: List[InstanceMetrics] = field(default_factory=list)
    consecutive_scale_up_ticks: int = 0
    consecutive_scale_down_ticks: int = 0
    last_scale_action: Optional[ScaleAction] = None
    last_scale_time: Optional[datetime] = None
    cooldown_until: Optional[datetime] = None
    is_frozen: bool = False
    redis_cache_hit_rate: float = 0.0
    active_users: int = 0
    max_submission_rps: float = 0.0


@dataclass
class ScaleEvent:
    service: str
    action: ScaleAction
    instance_count_before: int
    instance_count_after: int
    reason: str
    timestamp: datetime


class AutoScaler:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.services: Dict[str, ServiceState] = {
            name: ServiceState(name=name) for name in SERVICE_BOUNDS.keys()
        }
        self.scale_events: List[ScaleEvent] = []
        self.running = True
        self.manual_override_lock = threading.Lock()
        self.flask_app = Flask(__name__, template_folder='templates')
        self._setup_flask_routes()
        self.flask_thread = None
        
    def _setup_flask_routes(self):
        @self.flask_app.route('/scaler', methods=['GET'])
        def dashboard():
            return render_template('dashboard.html')
        
        @self.flask_app.route('/scaler/status', methods=['GET'])
        def get_status():
            return jsonify(self._get_status_json())
        
        @self.flask_app.route('/scaler/scale', methods=['POST'])
        def manual_scale():
            data = request.json
            service = data.get('service')
            action = data.get('action')
            
            if service not in self.services:
                return jsonify({"error": "Invalid service"}), 400
            
            with self.manual_override_lock:
                if action == 'scale_up':
                    self._scale_up(service, reason="Manual override")
                elif action == 'scale_down':
                    self._scale_down(service, reason="Manual override")
                elif action == 'freeze':
                    self.services[service].is_frozen = True
                elif action == 'unfreeze':
                    self.services[service].is_frozen = False
                else:
                    return jsonify({"error": "Invalid action"}), 400
            
            return jsonify({"status": "success"})
    
    def _get_status_json(self) -> Dict[str, Any]:
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {},
            "scale_events": [
                {
                    "service": e.service,
                    "action": e.action.value,
                    "instance_count_before": e.instance_count_before,
                    "instance_count_after": e.instance_count_after,
                    "reason": e.reason,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in self.scale_events[-20:]  # Last 20 events
            ],
            "recommended_actions": {}
        }
        
        for name, state in self.services.items():
            instances_data = []
            for inst in state.instances:
                instances_data.append({
                    "container_id": inst.container_id[:12],
                    "cpu_percent": inst.cpu_percent,
                    "memory_mb": inst.memory_mb,
                    "process_count": inst.process_count,
                    "queue_depth": inst.queue_depth,
                    "p95_latency_ms": inst.p95_latency_ms,
                    "is_overloaded": inst.is_overloaded,
                    "last_updated": inst.last_updated.isoformat()
                })
            
            status["services"][name] = {
                "instance_count": len(state.instances),
                "instances": instances_data,
                "last_scale_action": state.last_scale_action.value if state.last_scale_action else None,
                "last_scale_time": state.last_scale_time.isoformat() if state.last_scale_time else None,
                "cooldown_until": state.cooldown_until.isoformat() if state.cooldown_until else None,
                "is_frozen": state.is_frozen,
                "redis_cache_hit_rate": state.redis_cache_hit_rate,
                "active_users": state.active_users,
                "max_submission_rps": state.max_submission_rps,
                "min_instances": SERVICE_BOUNDS[name]["min"],
                "max_instances": SERVICE_BOUNDS[name]["max"]
            }
            
            # Calculate recommended action
            if state.is_frozen:
                status["recommended_actions"][name] = "frozen"
            elif state.cooldown_until and state.cooldown_until > datetime.utcnow():
                status["recommended_actions"][name] = "cooldown"
            elif len(state.instances) >= SERVICE_BOUNDS[name]["max"]:
                status["recommended_actions"][name] = "at_max"
            elif len(state.instances) <= SERVICE_BOUNDS[name]["min"]:
                status["recommended_actions"][name] = "at_min"
            else:
                status["recommended_actions"][name] = self._calculate_recommended_action(name)
        
        return status
    
    def _calculate_recommended_action(self, service_name: str) -> str:
        state = self.services[service_name]
        if not state.instances:
            return "scale_up"
        
        avg_cpu = sum(inst.cpu_percent for inst in state.instances) / len(state.instances)
        avg_queue = sum(inst.queue_depth for inst in state.instances) / len(state.instances)
        avg_latency = sum(inst.p95_latency_ms for inst in state.instances) / len(state.instances)
        
        if avg_cpu > SCALE_UP_THRESHOLD_CPU or avg_queue > SCALE_UP_THRESHOLD_QUEUE or avg_latency > SCALE_UP_THRESHOLD_LATENCY:
            return "scale_up"
        elif avg_cpu < SCALE_DOWN_THRESHOLD_CPU and avg_queue < SCALE_DOWN_THRESHOLD_QUEUE:
            return "scale_down"
        
        return "no_action"
    
    def start_flask_server(self):
        self.flask_thread = threading.Thread(
            target=self.flask_app.run,
            kwargs={"host": "0.0.0.0", "port": 9090, "threaded": True},
            daemon=True
        )
        self.flask_thread.start()
        log.info("Flask API server started", port=9090)
    
    def collect_metrics(self):
        """Collect metrics from all running instances"""
        for service_name, state in self.services.items():
            try:
                # Get containers for this service
                containers = self.docker_client.containers.list(
                    filters={"label": f"skillnest.service={service_name}"}
                )
                
                # Update instance list
                current_ids = {c.id for c in containers}
                existing_ids = {inst.container_id for inst in state.instances}
                
                # Remove stopped containers
                state.instances = [inst for inst in state.instances if inst.container_id in current_ids]
                
                # Add new containers
                for container in containers:
                    if container.id not in existing_ids:
                        state.instances.append(InstanceMetrics(
                            container_id=container.id,
                            cpu_percent=0.0,
                            memory_mb=0.0,
                            process_count=0,
                            queue_depth=0,
                            p95_latency_ms=0.0,
                            is_overloaded=False,
                            last_updated=datetime.utcnow()
                        ))
                
                # Collect metrics for each instance
                for inst in state.instances:
                    try:
                        container = self.docker_client.containers.get(inst.container_id)
                        stats = container.stats(stream=False)
                        
                        # CPU calculation
                        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                                   stats["precpu_stats"]["cpu_usage"]["total_usage"]
                        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                                      stats["precpu_stats"]["system_cpu_usage"]
                        if system_delta > 0:
                            inst.cpu_percent = (cpu_delta / system_delta) * 100.0 * \
                                              len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [1]))
                        
                        # Memory
                        inst.memory_mb = stats["memory_stats"].get("usage", 0) / (1024 * 1024)
                        
                        # Process count (from pids)
                        inst.process_count = stats["pids_stats"].get("current", 0)
                        
                        # Service-specific metrics
                        if service_name == "springboot":
                            self._collect_springboot_metrics(container, inst)
                        elif service_name == "fastapi":
                            self._collect_fastapi_metrics(container, inst)
                        elif service_name == "executor":
                            self._collect_executor_metrics(container, inst)
                        
                        # Determine overload status
                        inst.is_overloaded = (
                            inst.cpu_percent > SCALE_UP_THRESHOLD_CPU or
                            inst.queue_depth > SCALE_UP_THRESHOLD_QUEUE or
                            inst.p95_latency_ms > SCALE_UP_THRESHOLD_LATENCY
                        )
                        
                        inst.last_updated = datetime.utcnow()
                        
                    except Exception as e:
                        log.error("Failed to collect metrics for instance",
                                 service=service_name, container_id=inst.container_id[:12], error=str(e))
                
                # Collect Redis metrics for Spring Boot
                if service_name == "springboot":
                    self._collect_redis_metrics(state)
                
                # Collect active users for rate limiting
                self._collect_active_users(state)
                
            except Exception as e:
                log.error("Failed to collect metrics for service", service=service_name, error=str(e))
    
    def _collect_springboot_metrics(self, container, inst: InstanceMetrics):
        """Collect metrics from Spring Boot Actuator"""
        try:
            # Get container IP
            container.reload()
            container_ip = container.attrs["NetworkSettings"]["Networks"]["skillnest-network"]["IPAddress"]
            
            # Try to get metrics from actuator
            response = requests.get(
                f"http://{container_ip}:8080/actuator/metrics/http.server.requests",
                timeout=2
            )
            if response.status_code == 200:
                metrics = response.json()
                # Extract queue depth and latency from metrics
                # This is simplified - in production, you'd parse the actual metrics
                inst.p95_latency_ms = metrics.get("measurements", [{}])[0].get("value", 0) * 1000
        except:
            pass  # Metrics collection failed, use defaults
    
    def _collect_fastapi_metrics(self, container, inst: InstanceMetrics):
        """Collect metrics from FastAPI Prometheus endpoint"""
        try:
            container.reload()
            container_ip = container.attrs["NetworkSettings"]["Networks"]["skillnest-network"]["IPAddress"]
            
            response = requests.get(f"http://{container_ip}:8000/metrics", timeout=2)
            if response.status_code == 200:
                # Parse Prometheus metrics
                lines = response.text.split('\n')
                for line in lines:
                    if line.startswith('http_request_duration_seconds_bucket{le="0.95"}'):
                        inst.p95_latency_ms = float(line.split(' ')[1]) * 1000
                        break
        except:
            pass
    
    def _collect_executor_metrics(self, container, inst: InstanceMetrics):
        """Collect metrics from Docker Executor"""
        try:
            # For executor, queue depth is the number of running containers
            executor_containers = self.docker_client.containers.list(
                filters={"label": "skillnest.executor=true"}
            )
            inst.queue_depth = len(executor_containers)
        except:
            pass
    
    def _collect_redis_metrics(self, state: ServiceState):
        """Collect Redis cache hit rate"""
        try:
            info = self.redis_client.info("stats")
            hits = info.get("keyspace_hits", 0)
            misses = info.get("keyspace_misses", 0)
            total = hits + misses
            if total > 0:
                state.redis_cache_hit_rate = (hits / total) * 100
        except:
            pass
    
    def _collect_active_users(self, state: ServiceState):
        """Collect active user count for rate limiting"""
        try:
            # Get active users from Redis (simplified - in production, use proper tracking)
            active_users = self.redis_client.scard("active_users")
            state.active_users = active_users if active_users > 0 else 100  # Default estimate
            # Calculate max submission RPS based on rate limit (30/min per user)
            state.max_submission_rps = (state.active_users * 30) / 60
        except:
            state.active_users = 100
            state.max_submission_rps = 50
    
    def evaluate_scaling(self):
        """Evaluate scaling decisions for all services"""
        for service_name, state in self.services.items():
            if state.is_frozen:
                continue
            
            # Check cooldown
            if state.cooldown_until and state.cooldown_until > datetime.utcnow():
                continue
            
            bounds = SERVICE_BOUNDS[service_name]
            current_count = len(state.instances)
            
            if not state.instances:
                # No instances, scale up to minimum
                if current_count < bounds["min"]:
                    self._scale_up(service_name, reason="No instances running")
                continue
            
            # Calculate averages
            avg_cpu = sum(inst.cpu_percent for inst in state.instances) / current_count
            avg_queue = sum(inst.queue_depth for inst in state.instances) / current_count
            avg_latency = sum(inst.p95_latency_ms for inst in state.instances) / current_count
            
            # Check scale-up conditions
            should_scale_up = (
                avg_cpu > SCALE_UP_THRESHOLD_CPU or
                avg_queue > SCALE_UP_THRESHOLD_QUEUE or
                avg_latency > SCALE_UP_THRESHOLD_LATENCY
            )
            
            # Check scale-down conditions
            should_scale_down = (
                avg_cpu < SCALE_DOWN_THRESHOLD_CPU and
                avg_queue < SCALE_DOWN_THRESHOLD_QUEUE
            )
            
            # Redis-aware scaling for Spring Boot
            if service_name == "springboot" and state.redis_cache_hit_rate > 80:
                should_scale_down = True
                log.info("Redis cache hit rate high, considering scale down",
                         service=service_name, hit_rate=state.redis_cache_hit_rate)
            
            # Rate-limit awareness for executor
            if service_name == "executor":
                current_rps = avg_queue  # Simplified: use queue depth as proxy
                if current_rps > state.max_submission_rps:
                    log.info("Rate limit reached, capping executor scale up",
                             service=service_name, current_rps=current_rps,
                             max_rps=state.max_submission_rps)
                    should_scale_up = False
            
            # Apply consecutive tick logic
            if should_scale_up:
                state.consecutive_scale_up_ticks += 1
                state.consecutive_scale_down_ticks = 0
            elif should_scale_down:
                state.consecutive_scale_down_ticks += 1
                state.consecutive_scale_up_ticks = 0
            else:
                state.consecutive_scale_up_ticks = 0
                state.consecutive_scale_down_ticks = 0
            
            # Execute scale actions
            if should_scale_up and state.consecutive_scale_up_ticks >= SCALE_UP_CONSECUTIVE_TICKS:
                if current_count < bounds["max"]:
                    self._scale_up(service_name, reason=f"High load: CPU {avg_cpu:.1f}%, Queue {avg_queue:.1f}, Latency {avg_latency:.1f}ms")
                    state.consecutive_scale_up_ticks = 0
            
            elif should_scale_down and state.consecutive_scale_down_ticks >= SCALE_DOWN_CONSECUTIVE_TICKS:
                if current_count > bounds["min"]:
                    self._scale_down(service_name, reason=f"Low load: CPU {avg_cpu:.1f}%, Queue {avg_queue:.1f}")
                    state.consecutive_scale_down_ticks = 0
    
    def _scale_up(self, service_name: str, reason: str):
        """Scale up a service by adding a new instance"""
        bounds = SERVICE_BOUNDS[service_name]
        state = self.services[service_name]
        current_count = len(state.instances)
        
        if current_count >= bounds["max"]:
            log.warning("Cannot scale up - at max instances", service=service_name, max=bounds["max"])
            return
        
        log.info("Scaling up service", service=service_name, current=current_count, reason=reason)
        
        try:
            # Create new container
            container_name = f"skillnest-{service_name}-{int(time.time())}"
            environment = {
                "DATABASE_URL": DB_URL,
                "REDIS_HOST": REDIS_HOST,
                "REDIS_PORT": str(REDIS_PORT),
                "JWT_SECRET": JWT_SECRET,
            }
            
            # Service-specific environment variables
            if service_name == "springboot":
                environment.update({
                    "SPRING_DATASOURCE_URL": DB_URL.replace("postgresql://", "jdbc:postgresql://"),
                    "SPRING_DATASOURCE_USERNAME": "skillnest",
                    "SPRING_DATASOURCE_PASSWORD": "skillnest",
                    "SPRING_DATA_REDIS_HOST": REDIS_HOST,
                    "SPRING_DATA_REDIS_PORT": str(REDIS_PORT),
                })
            elif service_name == "fastapi":
                environment.update({
                    "OLLAMA_BASE_URL": "http://ollama:11434",
                    "OLLAMA_MODEL": "lama3.1:8b",
                })
            
            container = self.docker_client.containers.run(
                bounds["image"],
                name=container_name,
                environment=environment,
                labels={"skillnest.service": service_name},
                network="skillnest-network",
                detach=True,
                publish_all_ports=True
            )
            
            log.info("Container started", service=service_name, container_id=container.id[:12])
            
            # Update Nginx config
            self._update_nginx_config(service_name)
            
            # Record scale event
            self.scale_events.append(ScaleEvent(
                service=service_name,
                action=ScaleAction.SCALE_UP,
                instance_count_before=current_count,
                instance_count_after=current_count + 1,
                reason=reason,
                timestamp=datetime.utcnow()
            ))
            
            # Update state
            state.last_scale_action = ScaleAction.SCALE_UP
            state.last_scale_time = datetime.utcnow()
            state.cooldown_until = datetime.utcnow() + timedelta(seconds=COOLDOWN_SECONDS)
            
        except Exception as e:
            log.error("Failed to scale up service", service=service_name, error=str(e))
    
    def _scale_down(self, service_name: str, reason: str):
        """Scale down a service by removing an instance"""
        bounds = SERVICE_BOUNDS[service_name]
        state = self.services[service_name]
        current_count = len(state.instances)
        
        if current_count <= bounds["min"]:
            log.warning("Cannot scale down - at min instances", service=service_name, min=bounds["min"])
            return
        
        log.info("Scaling down service", service=service_name, current=current_count, reason=reason)
        
        try:
            # Select instance to remove (least loaded)
            instance_to_remove = min(state.instances, key=lambda i: i.cpu_percent)
            
            # Drain the instance
            self._drain_instance(instance_to_remove.container_id)
            
            # Stop and remove container
            container = self.docker_client.containers.get(instance_to_remove.container_id)
            container.stop()
            container.remove()
            
            log.info("Container removed", service=service_name, container_id=instance_to_remove.container_id[:12])
            
            # Update Nginx config
            self._update_nginx_config(service_name)
            
            # Record scale event
            self.scale_events.append(ScaleEvent(
                service=service_name,
                action=ScaleAction.SCALE_DOWN,
                instance_count_before=current_count,
                instance_count_after=current_count - 1,
                reason=reason,
                timestamp=datetime.utcnow()
            ))
            
            # Update state
            state.last_scale_action = ScaleAction.SCALE_DOWN
            state.last_scale_time = datetime.utcnow()
            state.cooldown_until = datetime.utcnow() + timedelta(seconds=COOLDOWN_SECONDS)
            
        except Exception as e:
            log.error("Failed to scale down service", service=service_name, error=str(e))
    
    def _drain_instance(self, container_id: str):
        """Drain an instance before removal"""
        try:
            container = self.docker_client.containers.get(container_id)
            
            # Remove from Nginx upstream (temporarily)
            self._update_nginx_config_for_drain(container_id)
            
            # Wait for in-flight requests
            log.info("Draining instance", container_id=container_id[:12])
            time.sleep(DRAIN_TIMEOUT_SECONDS)
            
        except Exception as e:
            log.error("Failed to drain instance", container_id=container_id[:12], error=str(e))
    
    def _update_nginx_config(self, service_name: str):
        """Update Nginx upstream configuration for a service"""
        try:
            state = self.services[service_name]
            bounds = SERVICE_BOUNDS[service_name]
            
            # Get container IPs
            servers = []
            for inst in state.instances:
                try:
                    container = self.docker_client.containers.get(inst.container_id)
                    container.reload()
                    container_ip = container.attrs["NetworkSettings"]["Networks"]["skillnest-network"]["IPAddress"]
                    servers.append(f"server {container_ip}:{bounds['port']};")
                except:
                    pass
            
            # Generate upstream config
            template = Template("""
upstream {{ service_name }} {
    {% for server in servers %}
    {{ server }}
    {% endfor %}
}
""")
            config = template.render(service_name=service_name, servers=servers)
            
            # Write to Nginx config file
            config_path = f"/etc/nginx/conf.d/{service_name}-upstream.conf"
            with open(config_path, 'w') as f:
                f.write(config)
            
            # Reload Nginx
            self._reload_nginx()
            
            log.info("Nginx config updated", service=service_name, servers=len(servers))
            
        except Exception as e:
            log.error("Failed to update Nginx config", service=service_name, error=str(e))
    
    def _update_nginx_config_for_drain(self, container_id: str):
        """Update Nginx config to drain a specific instance"""
        # Simplified - in production, you'd mark the server as down
        pass
    
    def _reload_nginx(self):
        """Reload Nginx configuration"""
        try:
            # Run nginx reload command
            nginx_container = self.docker_client.containers.get("skillnest-nginx")
            nginx_container.exec_run("nginx -s reload")
            log.info("Nginx reloaded")
        except:
            # Fallback: try to reload on host
            try:
                import subprocess
                subprocess.run(["nginx", "-s", "reload"], check=True)
            except:
                log.warning("Failed to reload Nginx")
    
    def run(self):
        """Main run loop"""
        log.info("Starting SkillNest Auto-Scaler")
        
        # Start Flask server
        self.start_flask_server()
        
        # Initialize instances
        self._initialize_instances()
        
        # Main loop
        while self.running:
            try:
                self.collect_metrics()
                self.evaluate_scaling()
                time.sleep(METRICS_INTERVAL)
            except Exception as e:
                log.error("Error in main loop", error=str(e))
                time.sleep(METRICS_INTERVAL)
        
        log.info("Auto-Scaler stopped")
    
    def _initialize_instances(self):
        """Initialize minimum instances for each service"""
        for service_name, bounds in SERVICE_BOUNDS.items():
            state = self.services[service_name]
            current_count = len(self.docker_client.containers.list(
                filters={"label": f"skillnest.service={service_name}"}
            ))
            
            if current_count < bounds["min"]:
                log.info("Initializing minimum instances", service=service_name, current=current_count, min=bounds["min"])
                for _ in range(bounds["min"] - current_count):
                    self._scale_up(service_name, reason="Initialization")
    
    def shutdown(self):
        """Graceful shutdown"""
        log.info("Shutting down Auto-Scaler")
        self.running = False
        if self.flask_thread:
            self.flask_thread.join(timeout=5)


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    log.info("Received shutdown signal", signal=signum)
    if 'scaler' in globals():
        scaler.shutdown()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    scaler = AutoScaler()
    scaler.run()
