package com.skillnest.dto;

import com.skillnest.entity.Language;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExecutionRequest {
    private String code;
    private Language language;
    private String input;
    private Integer timeLimit;
    private Integer memoryLimit;
}
