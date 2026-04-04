package com.skillnest.controller;

import com.skillnest.dto.ProblemCreateDto;
import com.skillnest.dto.ProblemDetailDto;
import com.skillnest.dto.ProblemResponseDto;
import com.skillnest.service.ProblemService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {
    
    @Autowired
    private ProblemService problemService;
    
    @PostMapping("/problems")
    public ResponseEntity<ProblemResponseDto> createProblem(@Valid @RequestBody ProblemCreateDto problemCreateDto) {
        ProblemResponseDto problem = problemService.createProblem(problemCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(problem);
    }
    
    @GetMapping("/problems/{id}/all-testcases")
    public ResponseEntity<ProblemDetailDto> getProblemWithAllTestCases(@PathVariable Long id) {
        ProblemDetailDto problem = problemService.getProblemDetailWithAllTestCases(id);
        return ResponseEntity.ok(problem);
    }
    
    @PutMapping("/problems/{id}")
    public ResponseEntity<ProblemResponseDto> updateProblem(
            @PathVariable Long id,
            @Valid @RequestBody ProblemCreateDto problemCreateDto) {
        ProblemResponseDto problem = problemService.updateProblem(id, problemCreateDto);
        return ResponseEntity.ok(problem);
    }
    
    @DeleteMapping("/problems/{id}")
    public ResponseEntity<Void> deleteProblem(@PathVariable Long id) {
        problemService.deleteProblem(id);
        return ResponseEntity.noContent().build();
    }
}
