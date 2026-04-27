package com.skillnest.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Service
@Slf4j
public class HealthCheckService {
    
    private static final String HEALTHY_INSTANCES_KEY = "loadbalancer:healthy_instances";
    private static final String INSTANCE_HEALTH_PREFIX = "loadbalancer:health:";
    private static final int HEALTH_CHECK_TIMEOUT_SECONDS = 5;
    private static final int HEALTH_CACHE_TTL_MINUTES = 2;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    public boolean isInstanceHealthy(String instanceUrl) {
        try {
            String cacheKey = INSTANCE_HEALTH_PREFIX + instanceUrl;
            
            Boolean cachedHealth = (Boolean) redisTemplate.opsForValue().get(cacheKey);
            if (cachedHealth != null) {
                log.debug("Using cached health status for {}: {}", instanceUrl, cachedHealth);
                return cachedHealth;
            }
            
            String healthUrl = instanceUrl + "/api/health";
            log.debug("Checking health for instance: {}", healthUrl);
            
            String response = restTemplate.getForObject(healthUrl, String.class);
            boolean isHealthy = response != null && response.contains("UP");
            
            redisTemplate.opsForValue().set(cacheKey, isHealthy, 
                HEALTH_CACHE_TTL_MINUTES, TimeUnit.MINUTES);
            
            log.info("Health check for {}: {}", instanceUrl, isHealthy ? "HEALTHY" : "UNHEALTHY");
            return isHealthy;
            
        } catch (Exception e) {
            log.error("Health check failed for {}: {}", instanceUrl, e.getMessage());
            String cacheKey = INSTANCE_HEALTH_PREFIX + instanceUrl;
            redisTemplate.opsForValue().set(cacheKey, false, 
                HEALTH_CACHE_TTL_MINUTES, TimeUnit.MINUTES);
            return false;
        }
    }
    
    public List<String> getHealthyInstances(List<String> allInstances) {
        return allInstances.stream()
                .filter(this::isInstanceHealthy)
                .toList();
    }
    
    public void markInstanceUnhealthy(String instanceUrl) {
        String cacheKey = INSTANCE_HEALTH_PREFIX + instanceUrl;
        redisTemplate.opsForValue().set(cacheKey, false, 
            HEALTH_CACHE_TTL_MINUTES, TimeUnit.MINUTES);
        log.warn("Marked instance as unhealthy: {}", instanceUrl);
    }
    
    public void clearHealthCache() {
        redisTemplate.delete(HEALTHY_INSTANCES_KEY);
        redisTemplate.delete(redisTemplate.keys(INSTANCE_HEALTH_PREFIX + "*"));
        log.info("Cleared health check cache");
    }
    
    public void refreshHealthCache(List<String> instances) {
        log.info("Refreshing health cache for {} instances", instances.size());
        instances.forEach(this::isInstanceHealthy);
    }
}
