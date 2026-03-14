package com.skillnest.service;

import com.skillnest.entity.Verdict;
import com.skillnest.repository.SubmissionRepository;
import com.skillnest.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.stream.Collectors;

@Service
@Transactional
public class LeaderboardService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private SubmissionRepository submissionRepository;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Cacheable(value = "leaderboard", unless = "#result == null")
    public List<LeaderboardEntryDto> getLeaderboard() {
        List<LeaderboardEntryDto> leaderboard = userRepository.findAll().stream()
                .map(user -> {
                    long acceptedCount = submissionRepository.countByUserIdAndVerdict(user.getId(), Verdict.ACCEPTED);
                    return LeaderboardEntryDto.builder()
                            .userId(user.getId())
                            .email(user.getEmail())
                            .problemsSolved((int) acceptedCount)
                            .rank(0) // Will be set after sorting
                            .build();
                })
                .sorted(Comparator.comparingInt(LeaderboardEntryDto::getProblemsSolved).reversed())
                .collect(Collectors.toList());
        
        // Set ranks
        for (int i = 0; i < leaderboard.size(); i++) {
            leaderboard.get(i).setRank(i + 1);
        }
        
        return leaderboard;
    }
}
