# SBTM Tool - Session-Based Test Management

A comprehensive web-based tool for managing exploratory testing sessions using the Session-Based Test Management (SBTM) methodology.

## Overview

SBTM Tool provides a structured approach to exploratory testing by organizing testing activities into time-boxed sessions with specific charters, tracking metrics, and managing testing artifacts. Built with modern web technologies, it offers an intuitive interface for test managers and testers to collaborate effectively.

## Features

### Core Functionality
- **Session Management**: Create, track, and manage exploratory testing sessions
- **Charter Management**: Define and reuse test charters for consistent testing approach
- **Time Tracking**: Built-in timing and TBS (Test, Bug, Setup) metrics tracking
- **Session Templates**: Reusable session configurations for common testing scenarios

### Organization & Collaboration
- **Multi-Project Support**: Organize testing activities across different projects
- **Tester Management**: Track individual tester contributions and expertise
- **Product Versions**: Associate sessions with specific product versions
- **Test Environments**: Manage and track different testing environments

### Documentation & Reporting
- **Rich Notes**: Markdown support for detailed session notes (up to 32K characters)
- **Document Management**: Attach and manage relevant testing documents
- **Statistics & Analytics**: Visual reporting on testing metrics and progress
- **Tag System**: Hierarchical tagging for enhanced organization and filtering

### Technical Features
- **Real-time Updates**: Live session tracking and collaboration
- **Health Monitoring**: Built-in health check endpoints for deployment monitoring
- **Database Flexibility**: Support for SQLite (development) and PostgreSQL (production)
- **Cloud Deployment Ready**: Docker and AWS deployment configurations included

## Technology Stack

- **Backend**: Python with NiceGUI framework
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Frontend**: Modern web UI with responsive design
- **Deployment**: Docker containerization with AWS and Heroku support
- **Analytics**: Plotly integration for data visualization

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/adamkwhite/sbtm-tool.git
cd sbtm-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser to `http://localhost:8080`

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Access the application at `http://localhost:8080`

## Configuration

### Environment Variables

- `PORT`: Application port (default: 8080)
- `HOST`: Application host (default: 0.0.0.0)
- `ENVIRONMENT`: Runtime environment (development/production)
- `DATABASE_URL`: Database connection string (default: sqlite:///sbtm.db)

### Development Mode
```bash
ENVIRONMENT=development python main.py
```

### Production Mode
```bash
ENVIRONMENT=production PORT=8080 python main.py
```

## Usage

### Creating a Testing Session

1. Navigate to the **Sessions** tab
2. Click "New Session" to create a session
3. Select or create a charter defining what to test
4. Assign testers and specify products/environments
5. Start the session timer and begin testing
6. Track time allocation using TBS metrics:
   - **T (Testing)**: Time spent on actual testing activities
   - **B (Bug Investigation)**: Time spent investigating and documenting bugs
   - **S (Setup)**: Time spent on environment setup and administrative tasks

### Managing Charters

1. Go to the **Charters** tab
2. Create reusable test charters with clear objectives
3. Associate charters with relevant documents and tags
4. Use charter templates for common testing patterns

### Viewing Statistics

The **Statistics** tab provides insights into:
- Session completion rates
- Time distribution across TBS metrics
- Tester productivity metrics
- Testing coverage by product/environment

## Deployment

### AWS Deployment

The repository includes AWS CloudFormation templates and deployment scripts:

```bash
./deploy.sh
```

See `README-deployment.md` for detailed deployment instructions.

### Heroku Deployment

The application includes a `Procfile` for Heroku deployment:

```bash
git push heroku main
```

## Project Structure

```
sbtm-tool/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── database/
│   ├── models.py          # SQLAlchemy database models
│   └── __init__.py
├── views/                 # UI components and views
│   ├── main_layout.py     # Main application layout
│   ├── session_view.py    # Session management interface
│   ├── charter_view.py    # Charter management interface
│   ├── statistics_view.py # Analytics and reporting
│   └── ...
├── aws/                   # AWS deployment configurations
├── docker-compose.yml     # Docker setup
├── Dockerfile            # Container configuration
└── Procfile              # Heroku deployment
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions, bug reports, or feature requests, please open an issue on GitHub.