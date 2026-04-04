package com.skillnest.repository;

import com.skillnest.entity.TestCase;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TestCaseRepository extends JpaRepository<TestCase, Long> {
    List<TestCase> findByProblemId(Long problemId);
    
    @Query("SELECT tc FROM TestCase tc WHERE tc.problem.id = :problemId AND tc.isHidden = false")
    List<TestCase>findVisibleTestCases(@Param("problemId") Long problemId);
}
