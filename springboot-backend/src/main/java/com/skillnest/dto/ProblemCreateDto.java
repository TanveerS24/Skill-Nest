package com.skillnest.dto;

import com.skillnest.entity.Difficulty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
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
public class ProblemCreateDto {
    
    @NotBlank(message = "Title cannot be blank")
    private String title;
    
    @NotBlank(message = "Description cannot be blank")
    private String description;
    
    @NotNull(message = "Difficulty cannot be null")
    private Difficulty difficulty;
    
    @Min(value = 1, message = "Time limit must be at least 1 second")
    @Builder.Default
    private Integer timeLimit = 5;
    
    @Min(value = 1, message = "Memory limit must be at least 1 MB")
    @Builder.Default
    private Integer memoryLimit = 256;
    
    @Valid
    private List<TestCaseDto> testCases;
}
