package com.skillnest.dto;

import com.skillnest.entity.Language;
import com.skillnest.entity.Verdict;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SubmissionResponseDto {
    
    private Long id;
    private Long userId;
    private Long problemId;
    private Language language;
    private String code;
    private Verdict verdict;
    private Double runtime;
    private Double memory;
    private String timeComplexity;
    private String spaceComplexity;
    private LocalDateTime createdAt;
}
