package com.skillnest.dto;

import com.skillnest.entity.Language;
import com.skillnest.entity.Verdict;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SubmissionCreateDto {
    
    @NotNull(message = "Problem ID cannot be null")
    private Long problemId;
    
    @NotNull(message = "Language cannot be null")
    private Language language;
    
    @NotBlank(message = "Code cannot be blank")
    private String code;
}
