# 🔧 Troubleshooting Guide

Common issues and their solutions.

## Database Issues

### Issue: "Connection refused" to PostgreSQL

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
```powershell
# Check if PostgreSQL container is running
docker ps

# If not running, start it
docker-compose up -d

# Check logs
docker logs my-postgres

# Verify connection
docker exec -it my-postgres psql -U Tanveer -d skillnest
```

### Issue: Database tables not created

**Symptoms:**
```
sqlalchemy.exc.ProgrammingError: relation "users" does not exist
```

**Solution:**
```powershell
cd backend
.\venv\Scripts\activate
python scripts\seed.py
```

### Issue: "relation already exists" error

**Solution:**
```powershell
# Drop and recreate database
docker exec -it my-postgres psql -U Tanveer -d postgres
DROP DATABASE skillnest;
CREATE DATABASE skillnest;
\q

# Re-run seed script
python scripts\seed.py
```

## Ollama Issues

### Issue: "Connection refused" to Ollama

**Symptoms:**
```
requests.exceptions.ConnectionError: Connection refused localhost:11434
```

**Solution:**
```powershell
# Check if Ollama is running
ollama list

# If not, start Ollama
# Windows: Start from Start Menu or Task Manager
# Linux/Mac: sudo systemctl start ollama

# Verify it's running
curl http://localhost:11434/api/version
```

### Issue: Model not found

**Symptoms:**
```
ollama.exceptions.ModelNotFoundError: model not found
```

**Solution:**
```powershell
# Pull required models
ollama pull llama3.2:3b-instruct-q4_K_M
ollama pull nomic-embed-text

# Verify they're installed
ollama list
```

### Issue: Ollama uses too much memory

**Solution:**
```powershell
# Use smaller model variant
ollama pull llama3.2:1b

# Update backend/app/config.py
OLLAMA_MODEL = "llama3.2:1b"
```

## Docker Execution Issues

### Issue: "Docker daemon not running"

**Symptoms:**
```
docker.errors.DockerException: Error while fetching server API version
```

**Solution:**
```powershell
# Windows: Start Docker Desktop
# Check system tray for Docker icon

# Linux: Start Docker service
sudo systemctl start docker

# Verify Docker is running
docker ps
```

### Issue: Permission denied accessing Docker

**Symptoms:**
```
PermissionError: [WinError 5] Access is denied
```

**Solution (Windows):**
1. Run Docker Desktop as Administrator
2. Add your user to "docker-users" group
3. Restart your computer

**Solution (Linux):**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Issue: Language image not found

**Symptoms:**
```
docker.errors.ImageNotFound: 404 Client Error: Not Found
```

**Solution:**
```powershell
# Pull the missing image
docker pull python:3.11-slim
docker pull node:20-slim
docker pull gcc:13
docker pull openjdk:17-slim

# Verify images
docker images
```

### Issue: Container timeout on first execution

**Symptoms:**
First submission takes very long or times out

**Solution:**
```powershell
# Pre-pull all images to avoid download during execution
docker pull python:3.11-slim
docker pull node:20-slim
docker pull gcc:13
docker pull openjdk:17-slim
```

## Frontend Issues

### Issue: Monaco Editor not loading

**Symptoms:**
Blank editor area or console errors about Monaco

**Solution:**
```powershell
cd frontend

# Clear node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Restart dev server
npm run dev
```

### Issue: "Cannot find module" errors

**Solution:**
```powershell
# Clear cache and rebuild
rm -rf node_modules .svelte-kit build
npm install
npm run dev
```

### Issue: Tailwind styles not applying

**Symptoms:**
UI looks unstyled

**Solution:**
```powershell
# Ensure postcss.config.js exists
# Ensure tailwind.config.js has correct content paths
# Restart dev server
npm run dev
```

### Issue: "Failed to fetch" API errors

**Symptoms:**
```
TypeError: Failed to fetch
Network request failed
```

**Solution:**
1. Check backend is running at `http://localhost:8000`
2. Verify CORS settings in backend
3. Check browser console for specific error
4. Try accessing `http://localhost:8000/docs` directly

## Backend Issues

### Issue: Module import errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Port already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```powershell
# Windows: Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Issue: JWT token expired

**Symptoms:**
```
401 Unauthorized: Token has expired
```

**Solution:**
1. Logout and login again
2. Or adjust token expiration in `backend/app/config.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
```

## Rate Limiting Issues

### Issue: "Rate limit exceeded"

**Symptoms:**
```
429 Too Many Requests: Rate limit exceeded
```

**Solution:**
Wait a minute or adjust rate limit in `backend/app/config.py`:
```python
RATE_LIMIT_SUBMISSIONS = "20/minute"  # Increase from 10
```

## Code Execution Issues

### Issue: All submissions get "Runtime Error"

**Symptoms:**
Every code submission fails with runtime error

**Solution:**
1. Check Docker daemon is running
2. Verify language images are pulled
3. Check backend logs for specific error
4. Test Docker manually:
```powershell
docker run --rm python:3.11-slim python -c "print('Hello')"
```

### Issue: "Time Limit Exceeded" on simple code

**Symptoms:**
Simple "Hello World" programs timeout

**Solution:**
1. Check if Docker containers are slow to start
2. Pre-pull images
3. Increase timeout in `backend/app/config.py`:
```python
EXECUTION_TIMEOUT = 5  # seconds
```

### Issue: Memory limit too restrictive

**Symptoms:**
Legitimate solutions get "Memory Limit Exceeded"

**Solution:**
Adjust in `backend/app/config.py`:
```python
DOCKER_MEMORY_LIMIT = "512m"  # Increase from 256m
```

## Admin Access Issues

### Issue: "Access denied. Admin credentials required"

**Symptoms:**
Can't login to admin dashboard

**Solution:**
```powershell
# Verify admin user exists
python scripts\seed.py

# Default admin credentials:
# Email: admin@skillnest.com
# Password: admin123

# Or create admin manually in database
# Update users SET role = 'admin' WHERE email = 'your@email.com';
```

### Issue: Regular user can access admin routes

**Symptoms:**
Admin guard not working

**Solution:**
Check `frontend/src/routes/admin/+layout.js` exists and has:
```javascript
if (!isAuthenticated || !user || user.role !== 'admin') {
    throw redirect(302, '/login');
}
```

## Performance Issues

### Issue: Slow page loads

**Solution:**
1. Check if database indexes exist
2. Verify no large queries without pagination
3. Check browser console for slow API calls
4. Monitor backend logs for slow queries

### Issue: High memory usage

**Symptoms:**
Backend consuming excessive RAM

**Solution:**
1. Check for Docker container leaks:
```powershell
docker ps -a  # Should be clean, no stopped containers
```
2. Adjust database connection pool:
```python
# backend/app/database.py
pool_size=5,      # Reduce from 10
max_overflow=10,  # Reduce from 20
```

## Authentication Issues

### Issue: Login successful but redirects to login again

**Symptoms:**
User can login but gets redirected back

**Solution:**
1. Check browser localStorage for token
2. Verify JWT token is being stored
3. Check browser console for errors
4. Clear localStorage and try again:
```javascript
// In browser console
localStorage.clear()
```

### Issue: "Invalid authentication credentials"

**Symptoms:**
Token validation fails

**Solution:**
1. Check SECRET_KEY matches in backend
2. Verify token is in correct format
3. Check token expiration
4. Logout and login again

## Development Issues

### Issue: Changes not reflecting

**Symptoms:**
Code changes don't appear in running app

**Solution:**

**Backend:**
```powershell
# Ensure --reload flag is used
uvicorn app.main:app --reload
```

**Frontend:**
```powershell
# Restart dev server
# Stop with Ctrl+C
npm run dev
```

### Issue: Hot reload not working

**Solution (Frontend):**
```powershell
# Clear .svelte-kit cache
rm -rf .svelte-kit
npm run dev
```

**Solution (Backend):**
```powershell
# Restart with reload
uvicorn app.main:app --reload
```

## Browser-Specific Issues

### Issue: CORS errors in browser

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' blocked by CORS policy
```

**Solution:**
Verify CORS settings in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: LocalStorage not persisting

**Solution:**
1. Check browser privacy settings
2. Disable "Block third-party cookies"
3. Try incognito mode to test
4. Clear browser cache

## System-Specific Issues

### Windows Specific

**Issue: PowerShell execution policy**
```
.\venv\Scripts\activate : File cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue: Path too long errors**
```
FileNotFoundError: [WinError 206] The filename or extension is too long
```

**Solution:**
Enable long paths in Windows:
1. Open Registry Editor
2. Navigate to: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. Set `LongPathsEnabled` to 1

### Linux/Mac Specific

**Issue: Permission denied on scripts**
```
bash: ./script.sh: Permission denied
```

**Solution:**
```bash
chmod +x script.sh
```

## Debugging Tips

### Enable Debug Mode

**Backend:**
```python
# backend/app/config.py
DEBUG = True
```

**Frontend:**
Open browser DevTools (F12) and check:
- Console for JavaScript errors
- Network tab for API calls
- Application tab for localStorage

### Check Logs

**Backend Logs:**
```powershell
# Backend runs in terminal, errors appear there
# Or redirect to file:
uvicorn app.main:app --reload > backend.log 2>&1
```

**Docker Logs:**
```powershell
docker logs my-postgres
```

**Frontend Logs:**
Browser console (F12 → Console)

### Test API Endpoints Manually

Use `http://localhost:8000/docs` for interactive API testing

Or use curl:
```powershell
# Test health
curl http://localhost:8000/health

# Test login
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@skillnest.com","password":"admin123"}'
```

## Still Having Issues?

1. **Check README.md** for setup instructions
2. **Check QUICKSTART.md** for faster setup
3. **Check ARCHITECTURE.md** for system design
4. **Check backend logs** for specific errors
5. **Check browser console** for frontend errors
6. **Verify all prerequisites** are installed
7. **Try the nuclear option:**
```powershell
# Stop everything
docker-compose down
docker system prune -a

# Delete virtual environments
rm -rf backend/venv frontend/node_modules

# Start fresh
# Follow QUICKSTART.md from scratch
```

## Common Error Messages Decoded

| Error | Meaning | Solution |
|-------|---------|----------|
| `Connection refused` | Service not running | Start the service |
| `404 Not Found` | Endpoint doesn't exist | Check URL spelling |
| `401 Unauthorized` | Not logged in or token expired | Login again |
| `403 Forbidden` | Insufficient permissions | Need admin role |
| `429 Too Many Requests` | Rate limit hit | Wait a minute |
| `500 Internal Server Error` | Backend crashed | Check backend logs |
| `ModuleNotFoundError` | Missing dependency | Run pip/npm install |
| `EADDRINUSE` | Port already in use | Kill process or use different port |

---

**Pro Tip**: When reporting issues, include:
1. Full error message
2. Backend logs
3. Browser console logs
4. Steps to reproduce
5. Your environment (OS, Python version, Node version)
