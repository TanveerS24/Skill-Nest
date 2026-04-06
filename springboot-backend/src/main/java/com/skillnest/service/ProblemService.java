package com.skillnest.service;

import com.skillnest.dto.ProblemCreateDto;
import com.skillnest.dto.ProblemDetailDto;
import com.skillnest.dto.ProblemResponseDto;
import com.skillnest.dto.TestCaseDto;
import com.skillnest.entity.Problem;
import com.skillnest.entity.TestCase;
import com.skillnest.entity.Difficulty;
import com.skillnest.exception.ResourceNotFoundException;
import com.skillnest.repository.ProblemRepository;
import com.skillnest.repository.TestCaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class ProblemService {
    
    @Autowired
    private ProblemRepository problemRepository;
    
    @Autowired
    private TestCaseRepository testCaseRepository;
    
    public ProblemResponseDto createProblem(ProblemCreateDto problemCreateDto) {
        Problem problem = Problem.builder()
                .title(problemCreateDto.getTitle())
                .description(problemCreateDto.getDescription())
                .difficulty(problemCreateDto.getDifficulty())
                .timeLimit(problemCreateDto.getTimeLimit())
                .memoryLimit(problemCreateDto.getMemoryLimit())
                .build();
        
        Problem savedProblem = problemRepository.save(problem);
        
        if (problemCreateDto.getTestCases() != null && !problemCreateDto.getTestCases().isEmpty()) {
            for (TestCaseDto tcDto : problemCreateDto.getTestCases()) {
                TestCase testCase = TestCase.builder()
                        .problem(savedProblem)
                        .input(tcDto.getInput())
                        .expectedOutput(tcDto.getExpectedOutput())
                        .isHidden(tcDto.getIsHidden())
                        .build();
                testCaseRepository.save(testCase);
            }
        }
        
        return mapToDto(savedProblem);
    }
    
    public ProblemDetailDto getProblemDetail(Long problemId) {
        Problem problem = problemRepository.findById(problemId)
                .orElseThrow(() -> new ResourceNotFoundException("Problem not found"));
        
        List<TestCase> testCases = testCaseRepository.findVisibleTestCases(problemId);
        
        return ProblemDetailDto.builder()
                .id(problem.getId())
                .title(problem.getTitle())
                .description(problem.getDescription())
                .difficulty(problem.getDifficulty())
                .timeLimit(problem.getTimeLimit())
                .memoryLimit(problem.getMemoryLimit())
                .createdAt(problem.getCreatedAt())
                .testCases(testCases.stream()
                        .map(this::mapTestCaseToDto)
                        .collect(Collectors.toList()))
                .build();
    }
    
    public ProblemDetailDto getProblemDetailWithAllTestCases(Long problemId) {
        Problem problem = problemRepository.findById(problemId)
                .orElseThrow(() -> new ResourceNotFoundException("Problem not found"));
        
        List<TestCase> testCases = testCaseRepository.findByProblemId(problemId);
        
        return ProblemDetailDto.builder()
                .id(problem.getId())
                .title(problem.getTitle())
                .description(problem.getDescription())
                .difficulty(problem.getDifficulty())
                .timeLimit(problem.getTimeLimit())
                .memoryLimit(problem.getMemoryLimit())
                .createdAt(problem.getCreatedAt())
                .testCases(testCases.stream()
                        .map(this::mapTestCaseToDto)
                        .collect(Collectors.toList()))
                .build();
    }
    
    public Page<ProblemResponseDto> getAllProblems(Pageable pageable) {
        Page<Problem> problems = problemRepository.findAll(pageable);
        return new PageImpl<>(
                problems.getContent().stream()
                        .map(this::mapToDto)
                        .collect(Collectors.toList()),
                pageable,
                problems.getTotalElements()
        );
    }
    
    public Page<ProblemResponseDto> getProblemsByDifficulty(Difficulty difficulty, Pageable pageable) {
        Page<Problem> problems = problemRepository.findByDifficulty(difficulty, pageable);
        return new PageImpl<>(
                problems.getContent().stream()
                        .map(this::mapToDto)
                        .collect(Collectors.toList()),
                pageable,
                problems.getTotalElements()
        );
    }
    
    public ProblemResponseDto updateProblem(Long problemId, ProblemCreateDto problemCreateDto) {
        Problem problem = problemRepository.findById(problemId)
                .orElseThrow(() -> new ResourceNotFoundException("Problem not found"));
        
        problem.setTitle(problemCreateDto.getTitle());
        problem.setDescription(problemCreateDto.getDescription());
        problem.setDifficulty(problemCreateDto.getDifficulty());
        problem.setTimeLimit(problemCreateDto.getTimeLimit());
        problem.setMemoryLimit(problemCreateDto.getMemoryLimit());
        
        Problem updatedProblem = problemRepository.save(problem);
        return mapToDto(updatedProblem);
    }
    
    @SuppressWarnings("null")
public void deleteProblem(Long problemId) {
        Problem problem = problemRepository.findById(problemId)
                .orElseThrow(() -> new ResourceNotFoundException("Problem not found"));
        problemRepository.delete(problem);
    }
    
    private ProblemResponseDto mapToDto(Problem problem) {
        return ProblemResponseDto.builder()
                .id(problem.getId())
                .title(problem.getTitle())
                .description(problem.getDescription())
                .difficulty(problem.getDifficulty())
                .timeLimit(problem.getTimeLimit())
                .memoryLimit(problem.getMemoryLimit())
                .createdAt(problem.getCreatedAt())
                .build();
    }
    
    private TestCaseDto mapTestCaseToDto(TestCase testCase) {
        return TestCaseDto.builder()
                .id(testCase.getId())
                .input(testCase.getInput())
                .expectedOutput(testCase.getExpectedOutput())
                .isHidden(testCase.getIsHidden())
                .build();
    }
}
