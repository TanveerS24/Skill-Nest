package com.skillnest.controller;

import com.skillnest.dto.ExecutionRequest;
import com.skillnest.service.CodeExecutionService;
import com.skillnest.service.ExecutionResult;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/execute")
@Slf4j
public class ExecutionController {
    
    @Autowired
    private CodeExecutionService codeExecutionService;
    
    @PostMapping
    public ResponseEntity<ExecutionResult> executeCode(@RequestBody ExecutionRequest request) {
        log.info("Received remote execution request for language: {}", request.getLanguage());
        
        ExecutionResult result = codeExecutionService.executeCode(
                request.getCode(),
                request.getLanguage(),
                request.getInput(),
                request.getTimeLimit(),
                request.getMemoryLimit()
        );
        
        log.info("Execution completed with verdict: {}", result.getVerdict());
        return ResponseEntity.ok(result);
    }
}
