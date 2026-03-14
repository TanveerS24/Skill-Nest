package com.skillnest.repository;

import com.skillnest.entity.Submission;
import com.skillnest.entity.Verdict;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SubmissionRepository extends JpaRepository<Submission, Long> {
    Page<Submission> findByUserId(Long userId, Pageable pageable);
    Page<Submission> findByProblemId(Long problemId, Pageable pageable);
    Optional<Submission> findFirstByUserIdAndProblemIdOrderByCreatedAtDesc(Long userId, Long problemId);
    long countByUserIdAndVerdict(Long userId, Verdict verdict);
}
