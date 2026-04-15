package com.skillnest.service;

import com.skillnest.dto.UserCreateDto;
import com.skillnest.dto.UserLoginDto;
import com.skillnest.dto.UserResponseDto;
import com.skillnest.entity.User;
import com.skillnest.entity.UserRole;
import com.skillnest.exception.ResourceAlreadyExistsException;
import com.skillnest.exception.ResourceNotFoundException;
import com.skillnest.repository.UserRepository;
import com.skillnest.security.JwtProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;

@Service
@Transactional
public class AuthService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private JwtProvider jwtProvider;
    
    @SuppressWarnings("null")
    public UserResponseDto register(UserCreateDto userCreateDto) {
        if (userRepository.existsByEmail(userCreateDto.getEmail())) {
            throw new ResourceAlreadyExistsException("Email already registered");
        }
        
        User user = User.builder()
                .email(userCreateDto.getEmail())
                .password(passwordEncoder.encode(userCreateDto.getPassword()))
                .role(UserRole.USER)
                .build();
        
        User savedUser = userRepository.save(user);
        return mapToDto(savedUser);
    }
    
    public Map<String, Object> login(UserLoginDto userLoginDto) {
        User user = userRepository.findByEmail(userLoginDto.getEmail())
                .orElse(null);

        if (user == null || !passwordEncoder.matches(userLoginDto.getPassword(), user.getPassword())) {
            throw new IllegalArgumentException("Invalid email or password");
        }
        
        String accessToken = jwtProvider.generateAccessToken(
                user.getId().toString(),
                user.getEmail(),
                user.getRole().name()
        );

        String refreshToken = jwtProvider.generateRefreshToken(
                user.getId().toString(),
                user.getEmail(),
                user.getRole().name()
        );
        
        Map<String, Object> response = new HashMap<>();
        response.put("accessToken", accessToken);
        response.put("tokenType", "Bearer");
        response.put("refreshToken", refreshToken);
        response.put("user", mapToDto(user));
        
        return response;
    }
    
    public Map<String, Object> refreshAccessToken(String refreshToken) {
        if (!jwtProvider.validateToken(refreshToken)) {
            throw new IllegalArgumentException("Invalid refresh token");
        }
        
        String userId = jwtProvider.getUserIdFromJWT(refreshToken);
        String email = jwtProvider.getEmailFromJWT(refreshToken);
        String role = jwtProvider.getRoleFromJWT(refreshToken);
        
        String newAccessToken = jwtProvider.generateAccessToken(userId, email, role);
        
        Map<String, Object> response = new HashMap<>();
        response.put("accessToken", newAccessToken);
        response.put("tokenType", "Bearer");
        
        return response;
    }
    
    public User getCurrentUser(Long userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }
    
    public UserResponseDto getCurrentUserDto(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        return mapToDto(user);
    }
    
    public UserResponseDto mapToDto(User user) {
        return UserResponseDto.builder()
                .id(user.getId())
                .email(user.getEmail())
                .role(user.getRole())
                .createdAt(user.getCreatedAt())
                .build();
    }
}
