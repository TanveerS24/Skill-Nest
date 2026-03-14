package com.skillnest.repository;

import com.skillnest.entity.Problem;
import com.skillnest.entity.Difficulty;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ProblemRepository extends JpaRepository<Problem, Long> {
    Optional<Problem> findByTitle(String title);
    Page<Problem> findByDifficulty(Difficulty difficulty, Pageable pageable);
}
