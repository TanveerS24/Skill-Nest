package com.skillnest.service;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LeaderboardEntryDto {
    private Long userId;
    private String email;
    private Integer problemsSolved;
    private Integer rank;
}
