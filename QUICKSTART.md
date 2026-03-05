# SkillNest Quick Start Guide

Get SkillNest up and running in less than 5 minutes!

## Prerequisites

✅ Docker Desktop installed and running  
✅ That's it!

## Installation

### Windows

1. **Clone or download the project**
   ```powershell
   git clone <repository-url>
   cd skillnest
   ```

2. **Run the setup script**
   ```powershell
   .\setup.bat
   ```

3. **Wait for setup to complete** (2-3 minutes)

4. **Open your browser**
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

### Linux/macOS

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd skillnest
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Wait for setup to complete** (2-3 minutes)

4. **Open your browser**
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

## Demo Credentials

### Admin Account
- **Email:** admin@skillnest.com
- **Password:** admin123
- **Access:** Full platform access + admin dashboard

### User Account
- **Email:** user@test.com
- **Password:** user123
- **Access:** Problem solving and submissions

## First Steps

1. **Browse Problems (No Login Required)**
   - Visit http://localhost:5173/problems
   - View all 6 DSA problems
   - See difficulty levels and test cases

2. **Try Anonymous Features**
   - View leaderboard
   - Browse problem statements
   - Check test cases

3. **Login and Submit Code**
   - Click "Login" in top right
   - Use demo credentials
   - Select a problem
   - Choose your language (Python, Java, C, C++)
   - Write code in Monaco Editor
   - Submit and see real-time results

4. **Check Dashboard**
   - View your stats
   - See recent submissions
   - Track acceptance rate

5. **Admin Dashboard (Admin Only)**
   - Login as admin
   - Click "Admin" in navigation
   - View platform statistics
   - See most attempted problems
   - Check language usage

## Available Problems

1. **Two Sum** (Easy) - Array manipulation
2. **Valid Parentheses** (Easy) - Stack operations
3. **Reverse Linked List** (Easy) - Linked list operations
4. **Binary Search** (Easy) - Search algorithms
5. **Merge Sorted Arrays** (Medium) - Array merging
6. **Longest Substring** (Medium) - String algorithms

## Language Support

### Python
```python
def solution():
    # Your code here
    pass

if __name__ == "__main__":
    solution()
```

### Java
```java
public class Solution {
    public static void main(String[] args) {
        // Your code here
    }
}
```

### C
```c
#include <stdio.h>

int main() {
    // Your code here
    return 0;
}
```

### C++
```cpp
#include <iostream>
using namespace std;

int main() {
    // Your code here
    return 0;
}
```

## Features to Try

### 🔒 Secure Execution
- All code runs in isolated Docker containers
- Network access disabled
- Memory and CPU limits enforced
- Safe from malicious code

### 🤖 AI Analysis
- Automatic complexity estimation
- Security vulnerability detection
- Real-time feedback

### 🏆 Leaderboard
- Sort by problems solved
- Sort by time complexity
- Sort by space complexity
- Real-time rankings

### 📊 Analytics
- Personal dashboard
- Submission history
- Acceptance rate tracking
- Language usage stats

## Common Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Services
```bash
docker-compose restart
```

### Reset Everything
```bash
docker-compose down -v
./setup.sh  # or setup.bat on Windows
```

## Troubleshooting

### Can't access the site?
```bash
# Check if services are running
docker-compose ps

# Restart services
docker-compose restart
```

### Code execution fails?
```bash
# Pull Docker images
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull gcc:13-alpine
```

### Database issues?
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres redis
cd backend
python seed.py
```

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🐛 Check [GitHub Issues](https://github.com/your-repo/issues)
- 💬 Join our community chat

## What's Next?

- Try solving all 6 problems
- Compete on the leaderboard
- Test different languages
- Explore the admin dashboard (if admin)
- Check the API documentation at http://localhost:8000/docs

---

Happy Coding! 🚀
