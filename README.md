# NarrativeLens

## Overview
NarrativeLens is a serverless AWS application that processes and analyzes narratives using a combination of collectors, parsers, and analyzers implemented as AWS Lambda functions.

![Project Architecture](diagrams/Project%20diagram.drawio.png)

## Project Structure

## Description
NarrativeLens is a production-ready web application designed for analyzing and understanding narratives in text. The application is fully deployable to AWS infrastructure, providing scalable and reliable text analysis capabilities.

## Features
- Cloud-based text analysis
- AWS deployment support
- Scalable architecture
- Text narrative processing
- Web-based interface

## Installation

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/NarrativeLens.git

# Navigate to the project directory
cd NarrativeLens

# Install dependencies
npm install
```

### AWS Deployment
1. Ensure you have AWS CLI installed and configured with appropriate credentials
2. Configure your AWS deployment settings in your project
3. Deploy using:
```bash
# Build the project
npm run build

# Deploy to AWS (specific command depends on your deployment setup)
npm run deploy
```

## Usage
### Local Development
```bash
# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Production
The application can be accessed through your AWS deployment URL once deployed.

## Project Structure 