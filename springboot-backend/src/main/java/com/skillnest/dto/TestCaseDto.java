package com.skillnest.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TestCaseDto {
    
    private Long id;
    
    @NotBlank(message = "Input cannot be blank")
    private String input;
    
    @NotBlank(message = "Expected output cannot be blank")
    private String expectedOutput;
    
    @Builder.Default
    private Boolean isHidden = false;
}
