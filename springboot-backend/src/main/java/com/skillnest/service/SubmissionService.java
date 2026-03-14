package com.skillnest.service;

import com.skillnest.dto.SubmissionCreateDto;
import com.skillnest.dto.SubmissionResponseDto;
import com.skillnest.entity.*;
import com.skillnest.exception.ResourceNotFoundException;
import com.skillnest.repository.ProblemRepository;
import com.skillnest.repository.SubmissionRepository;
import com.skillnest.repository.TestCaseRepository;
import com.skillnest.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class SubmissionService {
    
    @Autowired
    private SubmissionRepository submissionRepository;
    
    @Autowired
    private ProblemRepository problemRepository;
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private TestCaseRepository testCaseRepository;
    
    @Autowired
    private CodeExecutionService codeExecutionService;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    public SubmissionResponseDto submitCode(Long userId, SubmissionCreateDto submissionCreateDto) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        
        Problem problem = problemRepository.findById(submissionCreateDto.getProblemId())
                .orElseThrow(() -> new ResourceNotFoundException("Problem not found"));
        
        // Get all test cases including hidden ones
        List<TestCase> testCases = testCaseRepository.findByProblemId(problem.getId());
        
        // Execute code against all test cases
        Verdict finalVerdict = Verdict.ACCEPTED;
        Double totalRuntime = 0.0;
        Double maxMemory = 0.0;
        
        for (TestCase testCase : testCases) {
            ExecutionResult result = codeExecutionService.executeCode(
                    submissionCreateDto.getCode(),
                    submissionCreateDto.getLanguage(),
                    testCase.getInput(),
                    problem.getTimeLimit(),
                    problem.getMemoryLimit()
            );
            
            if (result.getVerdict() != Verdict.ACCEPTED) {
                finalVerdict = result.getVerdict();
                break;
            }
            
            if (result.getRuntime() != null) {
                totalRuntime += result.getRuntime();
            }
            if (result.getMemory() != null && result.getMemory() > maxMemory) {
                maxMemory = result.getMemory();
            }
        }
        
        // Create submission
        Submission submission = Submission.builder()
                .user(user)
                .problem(problem)
                .language(submissionCreateDto.getLanguage())
                .code(submissionCreateDto.getCode())
                .verdict(finalVerdict)
                .runtime(totalRuntime > 0 ? totalRuntime / testCases.size() : null)
                .memory(maxMemory > 0 ? maxMemory : null)
                .build();
        
        Submission savedSubmission = submissionRepository.save(submission);
        
        // Invalidate cache
        redisTemplate.delete("leaderboard:*");
        redisTemplate.delete("user:" + userId + ":stats");
        
        return mapToDto(savedSubmission);
    }
    
    public Page<SubmissionResponseDto> getUserSubmissions(Long userId, Pageable pageable) {
        Page<Submission> submissions = submissionRepository.findByUserId(userId, pageable);
        List<SubmissionResponseDto> dtos = submissions.getContent().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
        return new PageImpl<>(dtos, pageable, submissions.getTotalElements());
    }
    
    public Page<SubmissionResponseDto> getProblemSubmissions(Long problemId, Pageable pageable) {
        Page<Submission> submissions = submissionRepository.findByProblemId(problemId, pageable);
        List<SubmissionResponseDto> dtos = submissions.getContent().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
        return new PageImpl<>(dtos, pageable, submissions.getTotalElements());
    }
    
    public SubmissionResponseDto getSubmission(Long submissionId) {
        Submission submission = submissionRepository.findById(submissionId)
                .orElseThrow(() -> new ResourceNotFoundException("Submission not found"));
        return mapToDto(submission);
    }
    
    public Long getUserAcceptedProblems(Long userId) {
        return submissionRepository.countByUserIdAndVerdict(userId, Verdict.ACCEPTED);
    }
    
    private SubmissionResponseDto mapToDto(Submission submission) {
        return SubmissionResponseDto.builder()
                .id(submission.getId())
                .userId(submission.getUser().getId())
                .problemId(submission.getProblem().getId())
                .language(submission.getLanguage())
                .code(submission.getCode())
                .verdict(submission.getVerdict())
                .runtime(submission.getRuntime())
                .memory(submission.getMemory())
                .timeComplexity(submission.getTimeComplexity())
                .spaceComplexity(submission.getSpaceComplexity())
                .createdAt(submission.getCreatedAt())
                .build();
    }
}
