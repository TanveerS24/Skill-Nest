package com.skillnest.service;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import com.skillnest.entity.Verdict;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ExecutionResult {
    private Verdict verdict;
    private Double runtime;
    private Double memory;
    private String output;
    private String error;
}
