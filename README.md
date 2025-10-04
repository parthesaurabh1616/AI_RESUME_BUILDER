# AI Resume Builder

A powerful, AI-powered resume builder built with Streamlit and OpenAI GPT. Create professional, ATS-friendly resumes with the help of artificial intelligence.

## 🚀 Features

### 🤖 AI-Powered Content Generation
- **Professional Summary**: Generate compelling summaries using OpenAI GPT
- **Job Descriptions**: AI-assisted job description creation
- **Achievement Bullets**: Get suggestions for impactful achievements
- **Skills Suggestions**: AI-recommended skills based on your field
- **Cover Letter**: Generate personalized cover letters

### 📊 Advanced Dashboard
- **Real-time Progress Tracking**: Visual progress indicators
- **Resume Analytics**: Completion statistics and suggestions
- **ATS Optimization**: Analyze job descriptions for keyword optimization
- **Template Selection**: Choose from multiple professional templates

### 🎨 Professional Templates
- **Modern**: Clean, contemporary design
- **Creative**: Bold design for creative professionals
- **Minimal**: Simple, elegant layout
- **Technical**: Perfect for tech professionals

### 📥 Multiple Export Options
- **PDF Export**: Professional PDF generation
- **Word Document**: Editable Word format
- **Plain Text**: For online applications
- **JSON Export**: Data backup and integration

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Data Visualization**: Plotly
- **PDF Generation**: ReportLab
- **Styling**: Custom CSS with gradients and animations
- **Data Storage**: Session state management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/parthesaurabh1616/AI_RESUME_BUILDER.git
   cd AI_RESUME_BUILDER
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API Key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or enter it in the app when prompted.

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📱 Usage Guide

### 1. Dashboard
- View resume completion progress
- Access quick actions
- See key metrics and features

### 2. Personal Information
- Enter basic contact details
- Write professional summary
- Add social media links
- Use AI to generate summaries

### 3. Work Experience
- Add job positions and companies
- Describe responsibilities and achievements
- Use AI to enhance descriptions
- Manage multiple experiences

### 4. Skills & Technologies
- Select from categorized skill lists
- Visualize skills distribution
- Add custom skills
- Track skill categories

### 5. AI Assistant
- Generate content for any section
- Analyze resume completeness
- Get ATS optimization suggestions
- Improve existing content

### 6. Templates
- Choose from professional templates
- Preview different styles
- Select ATS-friendly designs
- Customize appearance

### 7. Preview
- Real-time resume preview
- Template switching
- Quick statistics
- Format validation

### 8. Export
- Generate PDF documents
- Export to Word format
- Download as JSON
- Save as plain text

## 🎯 AI Features

### Content Generation
The AI assistant can help you create:
- **Professional summaries** tailored to your role
- **Job descriptions** with proper formatting
- **Achievement bullets** with metrics and impact
- **Skills suggestions** based on your field
- **Cover letters** personalized to job applications

### ATS Optimization
- Analyze job descriptions for keywords
- Suggest improvements for ATS compatibility
- Optimize content for specific roles
- Ensure proper formatting and structure

### Resume Analysis
- Calculate completion percentage
- Identify missing sections
- Suggest improvements
- Track progress over time

## 🎨 Customization

### Templates
Choose from multiple professional templates:
- **Modern**: Clean, contemporary design with subtle colors
- **Creative**: Bold design perfect for creative professionals
- **Minimal**: Simple, elegant layout focused on content
- **Technical**: Structured design ideal for tech roles

### Styling
The application uses custom CSS with:
- Gradient backgrounds
- Hover animations
- Professional color schemes
- Responsive design
- Modern typography

## 📊 Analytics

### Progress Tracking
- Visual progress bars for each section
- Completion percentage calculation
- Missing section identification
- Improvement suggestions

### Resume Statistics
- Total sections completed
- Experience entries count
- Skills listed
- Template usage

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your-openai-api-key
```

### Customization Options
- Modify templates in the `templates` section
- Update skill categories in the `skill_categories` dictionary
- Customize AI prompts for different content types
- Adjust styling in the CSS section

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Local Deployment
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Saurabh Parthe**
- GitHub: [@parthesaurabh1616](https://github.com/parthesaurabh1616)
- LinkedIn: [Saurabh Parthe](https://linkedin.com/in/saurabh)
- Portfolio: [saurabh.dev](https://saurabh.dev)

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Streamlit team for the amazing framework
- ReportLab for PDF generation capabilities
- Plotly for data visualization

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Contact: saurabh@example.com
- Documentation: [GitHub Wiki](https://github.com/parthesaurabh1616/AI_RESUME_BUILDER/wiki)

---

⭐ **Star this repository if you found it helpful!**

🚀 **Built with love using Streamlit & OpenAI**
