package com.skillnest.dto;

import com.skillnest.entity.Difficulty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProblemResponseDto {
    
    private Long id;
    private String title;
    private String description;
    private Difficulty difficulty;
    private Integer timeLimit;
    private Integer memoryLimit;
    private LocalDateTime createdAt;
}
