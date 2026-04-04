package com.skillnest.controller;

import com.skillnest.dto.SubmissionCreateDto;
import com.skillnest.dto.SubmissionResponseDto;
import com.skillnest.service.SubmissionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/submissions")
public class SubmissionController {
    
    @Autowired
    private SubmissionService submissionService;
    
    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<SubmissionResponseDto> submitCode(
            @Valid @RequestBody SubmissionCreateDto submissionCreateDto,
            Authentication authentication) {
        Long userId = Long.parseLong(authentication.getPrincipal().toString());
        SubmissionResponseDto submission = submissionService.submitCode(userId, submissionCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(submission);
    }
    
    @GetMapping("/user")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<SubmissionResponseDto>> getUserSubmissions(
            Authentication authentication,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Long userId = Long.parseLong(authentication.getPrincipal().toString());
        Pageable pageable = PageRequest.of(page, size);
        Page<SubmissionResponseDto> submissions = submissionService.getUserSubmissions(userId, pageable);
        return ResponseEntity.ok(submissions);
    }
    
    @GetMapping("/problem/{problemId}")
    public ResponseEntity<Page<SubmissionResponseDto>> getProblemSubmissions(
            @PathVariable Long problemId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<SubmissionResponseDto> submissions = submissionService.getProblemSubmissions(problemId, pageable);
        return ResponseEntity.ok(submissions);
    }
    
    @GetMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<SubmissionResponseDto> getSubmission(@PathVariable Long id) {
        SubmissionResponseDto submission = submissionService.getSubmission(id);
        return ResponseEntity.ok(submission);
    }
}
