# Contributing to SkillNest

Thank you for your interest in contributing to SkillNest! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what is best for the community

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose
- Git

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/skillnest.git
   cd skillnest
   ```

2. **Set Up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure Environment**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your local configuration
   ```

5. **Start Services**
   ```bash
   docker-compose up -d postgres redis
   ```

6. **Initialize Database**
   ```bash
   cd backend
   python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
   python seed.py
   ```

## Development Workflow

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Development

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow the coding standards
   - Add tests for new features
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Backend tests
   cd backend
   pytest tests/
   
   # Frontend tests
   cd frontend
   npm run test
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve bug"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused
- Use async/await for I/O operations

**Example:**
```python
async def get_problem(db: AsyncSession, problem_id: int) -> Optional[Problem]:
    """
    Retrieve a problem by ID.
    
    Args:
        db: Database session
        problem_id: ID of the problem to retrieve
        
    Returns:
        Problem object if found, None otherwise
    """
    result = await db.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    return result.scalar_one_or_none()
```

### TypeScript/Svelte (Frontend)

- Use TypeScript for type safety
- Follow Svelte best practices
- Use meaningful variable names
- Keep components small and reusable
- Use TailwindCSS for styling

**Example:**
```typescript
interface Problem {
    id: number;
    title: string;
    difficulty: 'easy' | 'medium' | 'hard';
}

async function fetchProblems(): Promise<Problem[]> {
    const response = await fetch('/api/problems');
    return response.json();
}
```

### Code Organization

```
backend/
├── app/
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── utils/             # Utility functions

frontend/
├── src/
│   ├── lib/
│   │   ├── components/    # Reusable components
│   │   ├── api/           # API client
│   │   └── stores/        # State management
│   └── routes/            # Page components
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

Write tests for:
- API endpoints
- Database models
- Business logic
- Validation logic

**Example Test:**
```python
async def test_create_user(client, db):
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

### Frontend Tests

```bash
cd frontend
npm run test
```

Write tests for:
- Component rendering
- User interactions
- API integration
- Store logic

## Submitting Changes

1. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

3. **PR Requirements**
   - Clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes
   - All tests passing
   - Code reviewed and approved

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots
(If applicable)

## Related Issues
Fixes #(issue number)
```

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify it's reproducible
3. Gather relevant information

### Bug Report Template

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Windows 10, macOS 13]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.0.0]

**Screenshots:**
(If applicable)

**Additional Context:**
Any other relevant information
```

## Feature Requests

### Feature Request Template

```markdown
**Problem Statement:**
What problem does this solve?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
What other solutions did you consider?

**Additional Context:**
Any mockups, examples, or references
```

## Project Structure Guide

### Adding New API Endpoint

1. Define Pydantic schema in `schemas.py`
2. Add route in appropriate file under `routes/`
3. Implement business logic
4. Add tests
5. Update API documentation

### Adding New Frontend Page

1. Create page component in `routes/`
2. Add navigation link in layout
3. Implement UI using existing components
4. Add state management if needed
5. Test user interactions

### Adding New Database Model

1. Define model in `models.py`
2. Create migration (if using Alembic)
3. Update related schemas
4. Update seed data if needed
5. Test CRUD operations

## Code Review Process

All submissions require code review:

1. **Automated Checks**
   - Tests must pass
   - Linting must pass
   - No security vulnerabilities

2. **Human Review**
   - Code quality
   - Adherence to standards
   - Documentation completeness
   - Test coverage

3. **Approval**
   - At least one maintainer approval required
   - Address all feedback before merge

## Questions?

- Open an issue for general questions
- Tag maintainers for urgent matters
- Join our community chat (if available)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to SkillNest! 🚀
