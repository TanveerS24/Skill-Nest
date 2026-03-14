package com.skillnest.controller;

import com.skillnest.dto.ProblemCreateDto;
import com.skillnest.dto.ProblemDetailDto;
import com.skillnest.dto.ProblemResponseDto;
import com.skillnest.entity.Difficulty;
import com.skillnest.service.ProblemService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/problems")
public class ProblemController {
    
    @Autowired
    private ProblemService problemService;
    
    @PostMapping
    public ResponseEntity<ProblemResponseDto> createProblem(@Valid @RequestBody ProblemCreateDto problemCreateDto) {
        ProblemResponseDto problem = problemService.createProblem(problemCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(problem);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<ProblemDetailDto> getProblem(@PathVariable Long id) {
        ProblemDetailDto problem = problemService.getProblemDetail(id);
        return ResponseEntity.ok(problem);
    }
    
    @GetMapping
    public ResponseEntity<Page<ProblemResponseDto>> getAllProblems(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<ProblemResponseDto> problems = problemService.getAllProblems(pageable);
        return ResponseEntity.ok(problems);
    }
    
    @GetMapping("/difficulty/{difficulty}")
    public ResponseEntity<Page<ProblemResponseDto>> getProblemsByDifficulty(
            @PathVariable Difficulty difficulty,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<ProblemResponseDto> problems = problemService.getProblemsByDifficulty(difficulty, pageable);
        return ResponseEntity.ok(problems);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<ProblemResponseDto> updateProblem(
            @PathVariable Long id,
            @Valid @RequestBody ProblemCreateDto problemCreateDto) {
        ProblemResponseDto problem = problemService.updateProblem(id, problemCreateDto);
        return ResponseEntity.ok(problem);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProblem(@PathVariable Long id) {
        problemService.deleteProblem(id);
        return ResponseEntity.noContent().build();
    }
}
