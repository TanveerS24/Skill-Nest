package com.skillnest.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "test_cases")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TestCase {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "problem_id", nullable = false, foreignKey = @ForeignKey(name = "fk_testcase_problem"))
    private Problem problem;
    
    @NotBlank(message = "Input cannot be blank")
    @Column(nullable = false, columnDefinition = "TEXT")
    private String input;
    
    @NotBlank(message = "Expected output cannot be blank")
    @Column(nullable = false, columnDefinition = "TEXT")
    private String expectedOutput;
    
    @Column(nullable = false)
    private Boolean isHidden = false;
}
