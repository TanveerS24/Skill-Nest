import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models import User, Problem, TestCase, Difficulty
from app.auth import get_password_hash


async def seed_database():
    """Seed database with initial data"""
    async with AsyncSessionLocal() as db:
        # Create admin user
        admin = User(
            email="admin@skillnest.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        
        # Create test user
        test_user = User(
            email="user@test.com",
            password_hash=get_password_hash("user123"),
            role="user"
        )
        db.add(test_user)
        
        await db.flush()
        
        # Problem 1: Two Sum
        problem1 = Problem(
            title="Two Sum",
            description="""Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Constraints:**
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- Only one valid answer exists.""",
            difficulty=Difficulty.EASY,
            time_limit=5,
            memory_limit=256
        )
        db.add(problem1)
        await db.flush()
        
        # Test cases for Two Sum
        test_cases_1 = [
            TestCase(problem_id=problem1.id, input="[2,7,11,15]\n9", expected_output="[0,1]", is_hidden=False),
            TestCase(problem_id=problem1.id, input="[3,2,4]\n6", expected_output="[1,2]", is_hidden=False),
            TestCase(problem_id=problem1.id, input="[3,3]\n6", expected_output="[0,1]", is_hidden=True),
            TestCase(problem_id=problem1.id, input="[1,5,3,7,8,9]\n12", expected_output="[2,4]", is_hidden=True),
        ]
        for tc in test_cases_1:
            db.add(tc)
        
        # Problem 2: Valid Parentheses
        problem2 = Problem(
            title="Valid Parentheses",
            description="""Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

**Example 1:**
```
Input: s = "()"
Output: true
```

**Example 2:**
```
Input: s = "()[]{}"
Output: true
```

**Example 3:**
```
Input: s = "(]"
Output: false
```

**Constraints:**
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.""",
            difficulty=Difficulty.EASY,
            time_limit=5,
            memory_limit=256
        )
        db.add(problem2)
        await db.flush()
        
        test_cases_2 = [
            TestCase(problem_id=problem2.id, input="()", expected_output="true", is_hidden=False),
            TestCase(problem_id=problem2.id, input="()[]{}", expected_output="true", is_hidden=False),
            TestCase(problem_id=problem2.id, input="(]", expected_output="false", is_hidden=False),
            TestCase(problem_id=problem2.id, input="{[]}", expected_output="true", is_hidden=True),
            TestCase(problem_id=problem2.id, input="([)]", expected_output="false", is_hidden=True),
        ]
        for tc in test_cases_2:
            db.add(tc)
        
        # Problem 3: Reverse Linked List
        problem3 = Problem(
            title="Reverse Linked List",
            description="""Given the head of a singly linked list, reverse the list, and return the reversed list.

**Example 1:**
```
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
```

**Example 2:**
```
Input: head = [1,2]
Output: [2,1]
```

**Example 3:**
```
Input: head = []
Output: []
```

**Input Format:**
Space-separated integers representing the linked list.

**Output Format:**
Space-separated integers representing the reversed linked list.

**Constraints:**
- 0 <= list length <= 5000
- -5000 <= Node.val <= 5000""",
            difficulty=Difficulty.EASY,
            time_limit=5,
            memory_limit=256
        )
        db.add(problem3)
        await db.flush()
        
        test_cases_3 = [
            TestCase(problem_id=problem3.id, input="1 2 3 4 5", expected_output="5 4 3 2 1", is_hidden=False),
            TestCase(problem_id=problem3.id, input="1 2", expected_output="2 1", is_hidden=False),
            TestCase(problem_id=problem3.id, input="", expected_output="", is_hidden=True),
            TestCase(problem_id=problem3.id, input="1", expected_output="1", is_hidden=True),
        ]
        for tc in test_cases_3:
            db.add(tc)
        
        # Problem 4: Binary Search
        problem4 = Problem(
            title="Binary Search",
            description="""Given a sorted array of integers `nums` and a target value, return the index of the target if it is in the array. If not, return -1.

You must write an algorithm with O(log n) runtime complexity.

**Example 1:**
```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

**Example 2:**
```
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1
```

**Input Format:**
Line 1: Space-separated sorted integers
Line 2: Target integer

**Output Format:**
Index of target or -1

**Constraints:**
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All integers in nums are unique
- nums is sorted in ascending order""",
            difficulty=Difficulty.EASY,
            time_limit=5,
            memory_limit=256
        )
        db.add(problem4)
        await db.flush()
        
        test_cases_4 = [
            TestCase(problem_id=problem4.id, input="-1 0 3 5 9 12\n9", expected_output="4", is_hidden=False),
            TestCase(problem_id=problem4.id, input="-1 0 3 5 9 12\n2", expected_output="-1", is_hidden=False),
            TestCase(problem_id=problem4.id, input="5\n5", expected_output="0", is_hidden=True),
            TestCase(problem_id=problem4.id, input="1 2 3 4 5 6 7 8 9 10\n7", expected_output="6", is_hidden=True),
        ]
        for tc in test_cases_4:
            db.add(tc)
        
        # Problem 5: Merge Sorted Arrays
        problem5 = Problem(
            title="Merge Sorted Arrays",
            description="""You are given two sorted arrays `nums1` and `nums2`. Merge them into a single sorted array and return it.

**Example 1:**
```
Input: nums1 = [1,2,3], nums2 = [2,5,6]
Output: [1,2,2,3,5,6]
```

**Example 2:**
```
Input: nums1 = [1], nums2 = []
Output: [1]
```

**Input Format:**
Line 1: Space-separated integers for nums1 (or empty line)
Line 2: Space-separated integers for nums2 (or empty line)

**Output Format:**
Space-separated sorted integers

**Constraints:**
- 0 <= nums1.length, nums2.length <= 1000
- -10^9 <= nums1[i], nums2[j] <= 10^9
- Both arrays are sorted in ascending order""",
            difficulty=Difficulty.MEDIUM,
            time_limit=5,
            memory_limit=256
        )
        db.add(problem5)
        await db.flush()
        
        test_cases_5 = [
            TestCase(problem_id=problem5.id, input="1 2 3\n2 5 6", expected_output="1 2 2 3 5 6", is_hidden=False),
            TestCase(problem_id=problem5.id, input="1\n", expected_output="1", is_hidden=False),
            TestCase(problem_id=problem5.id, input="\n1", expected_output="1", is_hidden=True),
            TestCase(problem_id=problem5.id, input="1 3 5 7\n2 4 6 8", expected_output="1 2 3 4 5 6 7 8", is_hidden=True),
        ]
        for tc in test_cases_5:
            db.add(tc)
        
        # Problem 6: Longest Substring Without Repeating Characters
        problem6 = Problem(
            title="Longest Substring Without Repeating Characters",
            description="""Given a string `s`, find the length of the longest substring without repeating characters.

**Example 1:**
```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

**Example 2:**
```
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**
```
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
```

**Input Format:**
String s

**Output Format:**
Integer representing the length

**Constraints:**
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces.""",
            difficulty=Difficulty.MEDIUM,
            time_limit=5,
            memory_limit=256
        )
        db.add(problem6)
        await db.flush()
        
        test_cases_6 = [
            TestCase(problem_id=problem6.id, input="abcabcbb", expected_output="3", is_hidden=False),
            TestCase(problem_id=problem6.id, input="bbbbb", expected_output="1", is_hidden=False),
            TestCase(problem_id=problem6.id, input="pwwkew", expected_output="3", is_hidden=False),
            TestCase(problem_id=problem6.id, input="", expected_output="0", is_hidden=True),
            TestCase(problem_id=problem6.id, input="abcdef", expected_output="6", is_hidden=True),
        ]
        for tc in test_cases_6:
            db.add(tc)
        
        await db.commit()
        print("✓ Database seeded successfully!")
        print("  - Admin: admin@skillnest.com / admin123")
        print("  - User: user@test.com / user123")
        print("  - 6 DSA problems with test cases")


if __name__ == "__main__":
    asyncio.run(seed_database())
