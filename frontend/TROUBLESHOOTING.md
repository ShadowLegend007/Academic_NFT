# Frontend Troubleshooting Guide

## 🚨 Common Issues and Solutions

### 1. **Forms Not Working**
**Problem**: Login/signup forms don't submit or show errors.

**Solutions**:
- ✅ **Fixed**: Added proper form structure with `name` attributes
- ✅ **Fixed**: Added proper form validation
- ✅ **Fixed**: Added error handling and user feedback

**Test**: Go to `http://localhost:3000/test.html` and test the authentication section.

### 2. **JavaScript Errors**
**Problem**: Console shows JavaScript errors.

**Solutions**:
- ✅ **Fixed**: Added proper error handling in API calls
- ✅ **Fixed**: Added console logging for debugging
- ✅ **Fixed**: Added proper event listeners

**Debug**: Open browser console (F12) and check for errors.

### 3. **Backend Connection Issues**
**Problem**: Frontend can't connect to backend.

**Solutions**:
- Ensure backend is running: `python start.py`
- Check backend URL in `js/api.js`: `const API_BASE_URL = 'http://localhost:8000'`
- Test connection at: `http://localhost:3000/test.html`

### 4. **CORS Errors**
**Problem**: Browser blocks requests due to CORS policy.

**Solutions**:
- Backend should have CORS configured (already done)
- Use the test page to verify connection
- Check browser console for CORS errors

### 5. **File Upload Not Working**
**Problem**: File upload button doesn't work.

**Solutions**:
- ✅ **Fixed**: Added proper file input handling
- ✅ **Fixed**: Added file type validation
- ✅ **Fixed**: Added upload progress tracking

### 6. **Authentication Issues**
**Problem**: Login/registration doesn't work.

**Solutions**:
- ✅ **Fixed**: Added proper form validation
- ✅ **Fixed**: Added user feedback
- ✅ **Fixed**: Added session management

## 🔧 Quick Fixes

### Start Frontend Server
```bash
# Windows
cd frontend
start-frontend.bat

# Mac/Linux
cd frontend
chmod +x start-frontend.sh
./start-frontend.sh

# Manual
cd frontend
python -m http.server 3000
```

### Start Backend Server
```bash
# From project root
python start.py
```

### Test Everything
1. Start backend: `python start.py`
2. Start frontend: `cd frontend && python -m http.server 3000`
3. Open: `http://localhost:3000/test.html`
4. Test each section

## 📋 Testing Checklist

### ✅ Basic Functionality
- [ ] Frontend loads without errors
- [ ] Navigation between pages works
- [ ] Forms display properly
- [ ] JavaScript loads without errors

### ✅ Authentication
- [ ] Login form submits
- [ ] Registration form submits
- [ ] Error messages display
- [ ] Success messages display
- [ ] Redirects work after login

### ✅ API Integration
- [ ] Backend connection test passes
- [ ] File upload works
- [ ] Error handling works
- [ ] Loading states display

### ✅ User Experience
- [ ] Responsive design works
- [ ] Loading animations work
- [ ] Toast notifications display
- [ ] Form validation works

## 🐛 Debug Mode

### Enable Debug Logging
The test page (`/test.html`) includes debug logging that shows:
- Console messages
- API responses
- Error details
- Authentication status

### Browser Console
Open browser console (F12) to see:
- JavaScript errors
- API request/response logs
- Authentication events
- Form submission events

## 🔄 Common Workflows

### New User Registration
1. Go to `/aptos_frontend/sign_up.html`
2. Fill in all fields
3. Submit form
4. Should redirect to dashboard

### Existing User Login
1. Go to `/aptos_frontend/login.html`
2. Enter email and password
3. Submit form
4. Should redirect to dashboard

### File Upload
1. Go to `/aptos_frontend/student_upload.html`
2. Enter document title
3. Select file
4. Click upload
5. Should show analysis results

## 📞 Getting Help

If you're still having issues:

1. **Check the test page**: `http://localhost:3000/test.html`
2. **Check browser console**: F12 → Console tab
3. **Check network tab**: F12 → Network tab
4. **Verify backend is running**: `http://localhost:8000/`

### Error Messages to Look For
- `Failed to fetch`: Backend not running or CORS issue
- `Form validation failed`: Missing required fields
- `Authentication failed`: Invalid credentials
- `Upload failed`: File type or size issue

## 🎯 Quick Test Commands

```bash
# Test backend
curl http://localhost:8000/

# Test frontend
curl http://localhost:3000/

# Check if ports are in use
netstat -an | grep :8000
netstat -an | grep :3000
``` 