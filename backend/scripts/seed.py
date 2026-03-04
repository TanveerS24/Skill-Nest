"""
Seed script to create initial data including admin user and sample problems
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models.user import User, UserRole
from app.models.problem import Problem, Difficulty
from app.utils.security import get_password_hash


async def seed_admin_user():
    """Create an admin user"""
    async with AsyncSessionLocal() as db:
        # Check if admin already exists
        result = await db.execute(
            select(User).where(User.email == "admin@skillnest.com")
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin = User(
            email="admin@skillnest.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.admin,
            score=0
        )
        
        db.add(admin)
        await db.commit()
        print("✅ Admin user created: admin@skillnest.com / admin123")


async def seed_sample_problems():
    """Create sample problems"""
    async with AsyncSessionLocal() as db:
        # Check if problems already exist
        result = await db.execute(select(Problem))
        existing = result.scalars().all()
        
        if existing:
            print(f"Found {len(existing)} existing problems")
            return
        
        problems = [
            Problem(
                title="Two Sum",
                difficulty=Difficulty.Easy,
                description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Reverse String",
                difficulty=Difficulty.Easy,
                description="""Write a function that reverses a string. The input string is given as an array of characters.

You must do this by modifying the input array in-place with O(1) extra memory.

Example:
Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Palindrome Number",
                difficulty=Difficulty.Easy,
                description="""Given an integer x, return true if x is a palindrome, and false otherwise.

Example:
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Valid Parentheses",
                difficulty=Difficulty.Medium,
                description="""Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.

Example:
Input: s = "()[]{}"
Output: true""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Binary Search",
                difficulty=Difficulty.Easy,
                description="""Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Merge Sorted Arrays",
                difficulty=Difficulty.Medium,
                description="""You are given two integer arrays nums1 and nums2, sorted in non-decreasing order. Merge nums1 and nums2 into a single array sorted in non-decreasing order.

Example:
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Maximum Subarray",
                difficulty=Difficulty.Medium,
                description="""Given an integer array nums, find the subarray with the largest sum, and return its sum.

Example:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Longest Common Subsequence",
                difficulty=Difficulty.Hard,
                description="""Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

Example:
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Climbing Stairs",
                difficulty=Difficulty.Easy,
                description="""You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top:
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step""",
                time_limit=2,
                memory_limit=256
            ),
            Problem(
                title="Trapping Rain Water",
                difficulty=Difficulty.Hard,
                description="""Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. 
In this case, 6 units of rain water (blue section) are being trapped.""",
                time_limit=2,
                memory_limit=256
            ),
        ]
        
        db.add_all(problems)
        await db.commit()
        print(f"✅ Created {len(problems)} sample problems")


async def main():
    """Main seed function"""
    print("Initializing database...")
    await init_db()
    
    print("\nSeeding admin user...")
    await seed_admin_user()
    
    print("\nSeeding sample problems...")
    await seed_sample_problems()
    
    print("\n✅ Database seeding completed!")
    print("\nAdmin credentials:")
    print("Email: admin@skillnest.com")
    print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(main())
