# Academic NFT Frontend

A modern, responsive frontend for the Academic NFT platform that allows students and teachers to manage academic credentials using blockchain technology.

## 🚀 Features

- **Student Features:**
  - Upload academic documents (PDF, DOCX, TXT)
  - Plagiarism detection and analysis
  - Mint academic credentials as NFTs
  - View and manage personal NFT collection
  - Dashboard with statistics and quick actions

- **Teacher Features:**
  - View student submissions
  - Verify academic credentials
  - Provide feedback on student work
  - Teacher-specific dashboard

- **General Features:**
  - Modern, responsive design with Tailwind CSS
  - Dark theme optimized for academic use
  - Real-time API integration
  - Authentication and role-based access
  - Mobile-friendly interface

## 📁 Project Structure

```
frontend/
├── index.html                 # Main landing page
├── dashboard.html             # Student dashboard
├── styles.css                 # Custom CSS styles
├── js/
│   ├── api.js                # API integration service
│   ├── auth.js               # Authentication handling
│   └── app.js                # Main application logic
├── aptos_frontend/           # Individual page components
│   ├── login.html            # Login page
│   ├── sign_up.html          # Student registration
│   ├── teacher_signup.html   # Teacher registration
│   ├── student_upload.html   # Document upload interface
│   ├── teacher_dashboard.html # Teacher dashboard
│   ├── home.html             # Alternative home page
│   ├── about_us.html         # About page
│   ├── contact_us.html       # Contact page
│   └── get_started.html      # Getting started guide
└── Img/                      # Image assets
    ├── Abhirup_datta_khan.jpg
    ├── Rituja_ganguly.jpg
    └── Subhodeep_mondal.jpg
```

## 🔧 Setup Instructions

### Prerequisites

1. **Backend Server**: Ensure your backend server is running (typically on `http://localhost:8000`)
2. **Web Server**: You can use any local web server to serve the frontend files

### Quick Start

1. **Start the Backend** (from project root):
   ```bash
   python start.py
   ```

2. **Serve the Frontend**:
   You can use Python's built-in server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   
   Or use Node.js http-server:
   ```bash
   npx http-server -p 3000
   ```

3. **Access the Application**:
   Open your browser and navigate to `http://localhost:3000`

### Configuration

The frontend is configured to connect to the backend API. You can modify the API endpoint in `js/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Update this to match your backend URL
```

## 🔌 API Integration

The frontend integrates with the following backend endpoints:

### Authentication Endpoints
- `POST /upload` - Upload academic documents
- `POST /analyze` - Analyze documents for plagiarism
- `POST /mint` - Mint documents as NFTs
- `GET /nfts` - Retrieve user's NFTs
- `POST /feedback` - Submit feedback
- `POST /teacher/comment` - Teacher comments

### API Service Features
- Automatic error handling and user feedback
- File upload with progress tracking
- Authentication token management
- Request/response interceptors

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#1383eb` - Main actions and highlights
- **Background Dark**: `#111a22` - Main background
- **Card Background**: `#192733` - Card and component backgrounds
- **Border Color**: `#233648` - Borders and dividers
- **Text Primary**: `#ffffff` - Primary text
- **Text Secondary**: `#92aec9` - Secondary text

### Typography
- **Primary Font**: Space Grotesk (for headings)
- **Secondary Font**: Noto Sans (for body text)
- **Font Weights**: 400, 500, 700, 900

### Components
- Responsive cards with hover effects
- Custom form inputs with focus states
- Loading animations and progress indicators
- Toast notifications for user feedback
- Modal dialogs for complex interactions

## 🔐 Authentication Flow

1. **Registration**: Users can register as students or teachers
2. **Login**: Email/password authentication
3. **Session Management**: JWT tokens stored in localStorage
4. **Role-based Access**: Different interfaces for students and teachers
5. **Protected Routes**: Automatic redirection for unauthenticated users

## 📱 Responsive Design

The frontend is fully responsive and optimized for:
- **Desktop**: Full-featured interface with sidebars and detailed views
- **Tablet**: Adapted layout with touch-friendly controls
- **Mobile**: Streamlined interface with essential features

## 🚀 Development

### Adding New Pages

1. Create a new HTML file in the `aptos_frontend/` directory
2. Include the required scripts:
   ```html
   <script src="../js/api.js"></script>
   <script src="../js/auth.js"></script>
   <script src="../js/app.js"></script>
   ```
3. Add page-specific logic in `js/app.js`

### Styling Guidelines

- Use Tailwind CSS classes for styling
- Follow the established color palette
- Ensure responsive design
- Maintain accessibility standards

### JavaScript Architecture

- **api.js**: Handles all backend communication
- **auth.js**: Manages authentication and user sessions
- **app.js**: Main application logic and page-specific handlers

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend has CORS properly configured
2. **API Connection**: Check that the backend server is running and accessible
3. **File Upload Issues**: Verify file size limits and supported formats
4. **Authentication**: Clear localStorage if experiencing login issues

### Debug Mode

Enable debug logging by opening the browser console. The application logs important events and errors for debugging.

## 📄 License

This frontend is part of the Academic NFT project. See the main project README for licensing information.

## 🤝 Contributing

1. Follow the existing code style and structure
2. Test changes across different screen sizes
3. Ensure all API integrations work correctly
4. Update documentation for any new features

## 📞 Support

For technical support or questions about the frontend integration, please refer to the main project documentation or contact the development team. 