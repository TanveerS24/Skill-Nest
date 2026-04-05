package com.skillnest.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TokenDto {
    
    private String accessToken;
    @Builder.Default
    private String tokenType = "Bearer";
    
    @Builder.Default
    private Long expiresIn = 3600L;
}
