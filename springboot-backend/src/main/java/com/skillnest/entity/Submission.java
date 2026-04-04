package com.skillnest.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "submissions", indexes = {
    @Index(name = "idx_created_at", columnList = "created_at"),
    @Index(name = "idx_user_problem", columnList = "user_id,problem_id")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Submission {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, foreignKey = @ForeignKey(name = "fk_submission_user"))
    private User user;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "problem_id", nullable = false, foreignKey = @ForeignKey(name = "fk_submission_problem"))
    private Problem problem;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Language language;
    
    @Column(nullable = false, columnDefinition = "TEXT")
    private String code;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Verdict verdict;
    
    @Column
    private Double runtime; // milliseconds
    
    @Column
    private Double memory; // MB
    
    @Column(length = 50)
    private String timeComplexity;
    
    @Column(length = 50)
    private String spaceComplexity;
    
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
