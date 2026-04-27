package com.skillnest.service;

import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;

@Component
@ConfigurationProperties(prefix = "loadbalancer")
@Slf4j
@Getter
public class ManualLoadBalancer {
    
    private boolean enabled = true;
    private List<String> instances = new ArrayList<>();
    private final AtomicInteger roundRobinIndex = new AtomicInteger(0);
    private final Random random = new Random();
    
    public ManualLoadBalancer() {
        log.info("ManualLoadBalancer initialized");
    }
    
    public void setInstances(List<String> instances) {
        this.instances = instances;
        log.info("ManualLoadBalancer configured with {} instances: {}", instances.size(), instances);
    }
    
    public String getNextInstanceRoundRobin() {
        if (instances.isEmpty()) {
            throw new IllegalStateException("No instances configured for load balancing");
        }
        int index = roundRobinIndex.getAndUpdate(i -> (i + 1) % instances.size());
        String instance = instances.get(index);
        log.debug("Round Robin selected instance: {}", instance);
        return instance;
    }
    
    public String getNextInstanceRandom() {
        if (instances.isEmpty()) {
            throw new IllegalStateException("No instances configured for load balancing");
        }
        int index = random.nextInt(instances.size());
        String instance = instances.get(index);
        log.debug("Random selected instance: {}", instance);
        return instance;
    }
    
    public String getInstanceByIndex(int index) {
        if (instances.isEmpty()) {
            throw new IllegalStateException("No instances configured for load balancing");
        }
        if (index < 0 || index >= instances.size()) {
            throw new IllegalArgumentException("Invalid instance index: " + index);
        }
        return instances.get(index);
    }
    
    public List<String> getAllInstances() {
        return List.copyOf(instances);
    }
    
    public int getInstanceCount() {
        return instances.size();
    }
}
