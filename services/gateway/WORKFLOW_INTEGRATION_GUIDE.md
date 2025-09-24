# BHIV HR Platform - Workflow & Pipeline Integration Guide
**Version: 3.2.0 | Complete Integration System**

## 🚀 Overview

The BHIV HR Platform Gateway now features a comprehensive **Workflow & Pipeline Integration System** that orchestrates all 166+ API endpoints into structured, automated workflows with dependency management, error recovery, and real-time monitoring.

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Workflow Engine](#workflow-engine)
3. [Pipeline Orchestrator](#pipeline-orchestrator)
4. [Endpoint Registry](#endpoint-registry)
5. [Integration Components](#integration-components)
6. [Usage Examples](#usage-examples)
7. [API Reference](#api-reference)
8. [Monitoring & Analytics](#monitoring--analytics)
9. [Deployment Guide](#deployment-guide)

## 🏗️ System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    BHIV HR Gateway                          │
│                 Integrated System v3.2.0                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Workflow  │  │  Pipeline   │  │  Endpoint   │        │
│  │   Engine    │  │Orchestrator │  │  Registry   │        │
│  │             │  │             │  │             │        │
│  │ • Creation  │  │ • Templates │  │ • Schema    │        │
│  │ • Execution │  │ • Execution │  │ • Validation│        │
│  │ • Monitoring│  │ • Batch Ops │  │ • Analytics │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                   Core API Gateway                         │
│              166 REST API Endpoints                        │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│   │Candidates│ │  Jobs   │ │AI Match │ │Security │        │
│   │   (12)   │ │   (8)   │ │   (9)   │ │  (12)   │        │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│   │  Auth   │ │Interview│ │Monitor  │ │Analytics│        │
│   │  (15)   │ │   (8)   │ │  (22)   │ │  (15)   │        │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Integration Benefits

- **🔄 Automated Workflows**: Multi-step processes with dependency management
- **⚡ Pipeline Orchestration**: Batch operations and parallel execution
- **📊 Real-time Monitoring**: Status tracking and performance metrics
- **🛡️ Error Recovery**: Automatic retry logic and graceful degradation
- **📈 Analytics Integration**: Comprehensive workflow analytics
- **🔧 Extensibility**: Custom workflow and pipeline creation

## 🔄 Workflow Engine

### Workflow Types

The system supports 6 predefined workflow types:

#### 1. **Candidate Onboarding** (`candidate_onboarding`)
```json
{
  "workflow_type": "candidate_onboarding",
  "steps": [
    "validate_data",      // Validate candidate information
    "create_profile",     // Create candidate profile
    "extract_resume",     // Extract resume information
    "skill_analysis",     // Analyze skills & experience
    "ai_matching",        // Generate AI matches
    "send_welcome"        // Send welcome email
  ],
  "estimated_duration": "5-10 minutes"
}
```

#### 2. **Job Posting** (`job_posting`)
```json
{
  "workflow_type": "job_posting",
  "steps": [
    "validate_job",       // Validate job requirements
    "create_job",         // Create job posting
    "generate_description", // Generate job description
    "setup_matching",     // Setup AI matching criteria
    "publish_job",        // Publish job posting
    "notify_team"         // Notify hiring team
  ],
  "estimated_duration": "3-5 minutes"
}
```

#### 3. **Interview Process** (`interview_process`)
```json
{
  "workflow_type": "interview_process",
  "steps": [
    "schedule_interview", // Schedule interview
    "send_invites",       // Send calendar invites
    "prepare_materials",  // Prepare interview materials
    "conduct_interview",  // Conduct interview
    "collect_feedback",   // Collect feedback
    "update_status"       // Update candidate status
  ],
  "estimated_duration": "1-2 hours"
}
```

#### 4. **Hiring Pipeline** (`hiring_pipeline`)
```json
{
  "workflow_type": "hiring_pipeline",
  "steps": [
    "application_review", // Review application
    "initial_screening",  // Initial screening
    "technical_assessment", // Technical assessment
    "interview_rounds",   // Interview rounds
    "reference_check",    // Reference check
    "offer_generation",   // Generate offer
    "offer_approval",     // Offer approval
    "send_offer"          // Send offer letter
  ],
  "estimated_duration": "2-4 weeks"
}
```

#### 5. **Bulk Operations** (`bulk_operations`)
```json
{
  "workflow_type": "bulk_operations",
  "steps": [
    "validate_batch",     // Validate batch data
    "process_items",      // Process individual items
    "generate_reports",   // Generate processing reports
    "send_notifications"  // Send completion notifications
  ],
  "estimated_duration": "10-30 minutes"
}
```

### Workflow API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/workflows` | POST | Create new workflow |
| `/v1/workflows` | GET | List workflows with filtering |
| `/v1/workflows/{workflow_id}` | GET | Get workflow details |
| `/v1/workflows/{workflow_id}/start` | POST | Start workflow execution |
| `/v1/workflows/{workflow_id}/cancel` | POST | Cancel workflow |
| `/v1/workflows/{workflow_id}/steps` | GET | Get workflow steps |
| `/v1/workflows/{workflow_id}/steps/{step_id}/retry` | POST | Retry failed step |
| `/v1/workflows/analytics` | GET | Workflow analytics |
| `/v1/workflows/health` | GET | Workflow system health |

## ⚡ Pipeline Orchestrator

### Pipeline Templates

The system includes 5 predefined pipeline templates:

#### 1. **Complete Candidate Flow**
```json
{
  "template_id": "complete_candidate_flow",
  "name": "Complete Candidate Management Flow",
  "description": "End-to-end candidate processing pipeline",
  "steps": [
    {
      "step_name": "health_check",
      "endpoint_calls": [
        {"endpoint": "/health", "method": "GET"},
        {"endpoint": "/v1/database/health", "method": "GET"}
      ]
    },
    {
      "step_name": "create_candidate",
      "endpoint_calls": [
        {"endpoint": "/v1/candidates", "method": "POST"}
      ],
      "depends_on": ["health_check"]
    },
    {
      "step_name": "ai_matching",
      "endpoint_calls": [
        {"endpoint": "/v1/match/jobs", "method": "POST"},
        {"endpoint": "/v1/match/recommendations/{{candidate_id}}", "method": "GET"}
      ],
      "depends_on": ["create_candidate"]
    }
  ]
}
```

#### 2. **Job Posting Workflow**
- System validation and health checks
- Job creation and validation
- AI matching configuration
- Analytics generation

#### 3. **Interview Management Flow**
- Authentication and permissions
- Interview scheduling
- Calendar management
- Analytics tracking

#### 4. **Security Audit Pipeline**
- Security configuration validation
- Threat analysis
- Audit logging review
- Backup verification

#### 5. **System Monitoring & Health Check**
- Basic health checks
- Performance metrics collection
- Dependency verification
- Error analysis

### Pipeline API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/pipelines/templates` | GET | List pipeline templates |
| `/v1/pipelines/templates/{template_id}` | GET | Get template details |
| `/v1/pipelines/execute/{template_id}` | POST | Execute pipeline |
| `/v1/pipelines/batch-execute` | POST | Execute multiple pipelines |
| `/v1/pipelines/custom` | POST | Create custom pipeline |
| `/v1/pipelines/validate` | POST | Validate pipeline structure |
| `/v1/pipelines/analytics` | GET | Pipeline analytics |
| `/v1/pipelines/health` | GET | Pipeline system health |

## 📊 Endpoint Registry

### Registry Features

- **Complete Catalog**: All 166+ endpoints registered with metadata
- **Schema Validation**: Request/response schema documentation
- **Category Organization**: Endpoints grouped by functionality
- **Authentication Mapping**: Security requirements per endpoint
- **Rate Limiting Info**: Rate limiting configuration per endpoint

### Endpoint Categories

| Category | Count | Description |
|----------|-------|-------------|
| **Core** | 4 | Basic API and health endpoints |
| **Candidates** | 12 | Candidate management operations |
| **Jobs** | 8 | Job posting and management |
| **AI Matching** | 9 | AI-powered matching algorithms |
| **Authentication** | 15 | User authentication and authorization |
| **Interviews** | 8 | Interview scheduling and management |
| **Security** | 12 | Security testing and validation |
| **Sessions** | 6 | Session management |
| **Monitoring** | 22 | System monitoring and metrics |
| **Analytics** | 15 | Analytics and reporting |
| **Client Portal** | 6 | Client-specific operations |
| **CSP Management** | 4 | Content Security Policy |
| **Database** | 4 | Database operations |
| **Workflows** | 20+ | Workflow management (New) |
| **Pipelines** | 15+ | Pipeline orchestration (New) |

### Registry API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/registry/endpoints` | GET | List all endpoints with filtering |
| `/v1/registry/categories` | GET | List endpoint categories |
| `/v1/registry/endpoints/{endpoint_id}` | GET | Get endpoint details |
| `/v1/registry/schema` | GET | Get complete API schema |
| `/v1/registry/stats` | GET | Registry statistics |
| `/v1/registry/validate` | POST | Validate registry structure |

## 🔧 Integration Components

### Main Integration File

The system is unified through `main_integrated.py` which provides:

- **Enhanced Middleware**: Request tracing and performance monitoring
- **Unified Routing**: All workflow, pipeline, and registry endpoints
- **Background Tasks**: Asynchronous workflow execution
- **Error Handling**: Comprehensive error recovery
- **System Monitoring**: Real-time health and performance metrics

### Key Integration Features

```python
# Enhanced root endpoint with integration info
@app.get("/")
async def enhanced_root():
    return {
        "message": "BHIV HR Platform API Gateway - Integrated Workflow System",
        "version": "3.2.0",
        "total_endpoints": "180+",
        "features": {
            "core_api": "166 endpoints",
            "workflow_system": "20+ workflow endpoints",
            "pipeline_engine": "15+ pipeline endpoints",
            "endpoint_registry": "10+ registry endpoints"
        },
        "capabilities": [
            "Multi-step Workflow Orchestration",
            "Pipeline Automation Engine",
            "Real-time Status Tracking",
            "Dependency Management",
            "Error Recovery & Retry Logic"
        ]
    }
```

## 📝 Usage Examples

### 1. Create and Execute Workflow

```bash
# Create candidate onboarding workflow
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "candidate_onboarding",
    "metadata": {
      "candidate_data": {
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "FastAPI"]
      }
    }
  }'

# Response
{
  "workflow_id": "wf_abc12345",
  "workflow_type": "candidate_onboarding",
  "status": "pending",
  "steps": [...],
  "created_at": "2025-01-18T10:00:00Z"
}

# Start workflow execution
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/workflows/wf_abc12345/start"

# Check workflow status
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/workflows/wf_abc12345"
```

### 2. Execute Pipeline Template

```bash
# Execute complete candidate flow pipeline
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/pipelines/execute/complete_candidate_flow" \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "candidate_name": "Jane Smith",
      "candidate_email": "jane@example.com"
    }
  }'

# Response
{
  "execution_id": "exec_xyz789",
  "pipeline_name": "Complete Candidate Management Flow",
  "status": "started",
  "total_steps": 4,
  "estimated_duration": "8-16 minutes"
}
```

### 3. Query Endpoint Registry

```bash
# List all endpoints in candidates category
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/registry/endpoints?category=candidates"

# Get complete API schema
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/registry/schema"

# Get registry statistics
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/registry/stats"
```

### 4. Monitor System Integration

```bash
# Get integration status
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/integration/status"

# Get comprehensive metrics
curl "https://bhiv-hr-gateway-901a.onrender.com/v1/integration/metrics"

# Test integration system
curl -X POST "https://bhiv-hr-gateway-901a.onrender.com/v1/integration/test"
```

## 📊 Monitoring & Analytics

### Workflow Analytics

```json
{
  "total_workflows": 150,
  "success_rate": 92.5,
  "failure_rate": 7.5,
  "avg_execution_time_seconds": 180.5,
  "workflow_distribution": {
    "candidate_onboarding": 45,
    "job_posting": 32,
    "interview_process": 28,
    "hiring_pipeline": 25,
    "bulk_operations": 20
  }
}
```

### Pipeline Analytics

```json
{
  "total_templates": 5,
  "most_used_templates": [
    {"template_id": "complete_candidate_flow", "usage_count": 45},
    {"template_id": "job_posting_workflow", "usage_count": 32}
  ],
  "success_rate": 92.5,
  "avg_execution_time": "4.2 minutes",
  "performance_metrics": {
    "fastest_pipeline": "monitoring_health_check",
    "slowest_pipeline": "complete_candidate_flow",
    "most_reliable": "security_audit_pipeline"
  }
}
```

### System Health Monitoring

```json
{
  "status": "healthy",
  "components": {
    "workflow_engine": "healthy",
    "pipeline_orchestrator": "healthy", 
    "endpoint_registry": "healthy",
    "background_tasks": "healthy"
  },
  "metrics": {
    "total_endpoints": "180+",
    "active_workflows": 3,
    "pipeline_templates": 5,
    "uptime": "99.9%"
  }
}
```

## 🚀 Deployment Guide

### Local Development

```bash
# Clone repository
git clone https://github.com/shashankmishraa/BHIV-HR-Platform.git
cd BHIV-HR-Platform/services/gateway

# Install dependencies
pip install -r requirements.txt

# Run integrated system
python app/main_integrated.py

# Access integrated API
curl http://localhost:8000/
curl http://localhost:8000/v1/workflows
curl http://localhost:8000/v1/pipelines/templates
```

### Production Deployment

The integrated system is deployed on Render with the following services:

- **Gateway Service**: https://bhiv-hr-gateway-901a.onrender.com
- **Workflow Engine**: Embedded in gateway service
- **Pipeline Orchestrator**: Embedded in gateway service
- **Endpoint Registry**: Embedded in gateway service

### Environment Variables

```bash
# Required environment variables
ENVIRONMENT=production
DATABASE_URL=postgresql://...
API_KEY=your_api_key_here
CORS_ORIGINS=*
LOG_LEVEL=INFO
```

## 🔧 Configuration

### Workflow Configuration

```python
# Custom workflow definition
CUSTOM_WORKFLOW = {
    "workflow_type": "custom_process",
    "steps": [
        {
            "step_id": "validate",
            "name": "Validate Input Data",
            "timeout_seconds": 30,
            "retry_count": 3
        },
        {
            "step_id": "process",
            "name": "Process Data",
            "depends_on": ["validate"],
            "timeout_seconds": 60,
            "retry_count": 2
        }
    ]
}
```

### Pipeline Configuration

```python
# Custom pipeline template
CUSTOM_PIPELINE = {
    "name": "Custom Data Processing Pipeline",
    "description": "Process data through multiple endpoints",
    "steps": [
        {
            "step_name": "data_validation",
            "endpoint_calls": [
                {
                    "endpoint": "/v1/validate",
                    "method": "POST",
                    "body": {"data": "{{input_data}}"}
                }
            ]
        }
    ]
}
```

## 📚 API Reference

### Complete Endpoint List

The integrated system provides **180+ endpoints** across all categories:

- **Core API**: 166 original endpoints
- **Workflow System**: 20+ workflow management endpoints
- **Pipeline Engine**: 15+ pipeline orchestration endpoints  
- **Endpoint Registry**: 10+ registry and schema endpoints
- **Integration Management**: 5+ integration monitoring endpoints

### Authentication

Most endpoints require authentication via Bearer token:

```bash
curl -H "Authorization: Bearer your_api_key_here" \
     "https://bhiv-hr-gateway-901a.onrender.com/v1/workflows"
```

### Rate Limiting

- **Standard Endpoints**: 60 requests/minute
- **Workflow Operations**: 30 requests/minute
- **Pipeline Execution**: 10 executions/minute
- **Registry Queries**: 100 requests/minute

## 🎯 Benefits & Use Cases

### Business Benefits

1. **Automated Processes**: Reduce manual work through workflow automation
2. **Improved Efficiency**: Streamlined operations with pipeline orchestration
3. **Better Monitoring**: Real-time visibility into system operations
4. **Error Reduction**: Automated error handling and recovery
5. **Scalability**: Handle increased workload through automation

### Technical Benefits

1. **Modular Architecture**: Clean separation of concerns
2. **Extensibility**: Easy to add new workflows and pipelines
3. **Maintainability**: Well-structured codebase with clear interfaces
4. **Testability**: Comprehensive testing capabilities
5. **Documentation**: Complete API documentation and schemas

### Use Cases

- **HR Onboarding**: Automate complete candidate onboarding process
- **Job Management**: Streamline job posting and candidate matching
- **Interview Coordination**: Orchestrate interview scheduling and feedback
- **Security Audits**: Automated security validation and compliance
- **System Monitoring**: Continuous health monitoring and alerting
- **Bulk Operations**: Process large datasets efficiently
- **Custom Workflows**: Create organization-specific processes

## 🔮 Future Enhancements

### Planned Features

1. **Visual Workflow Designer**: Drag-and-drop workflow creation
2. **Advanced Scheduling**: Cron-based workflow scheduling
3. **Event-Driven Workflows**: Trigger workflows based on events
4. **Workflow Templates**: Pre-built industry-specific workflows
5. **Integration Connectors**: Connect with external systems
6. **Machine Learning**: AI-powered workflow optimization
7. **Mobile Dashboard**: Mobile app for workflow monitoring
8. **Multi-tenant Support**: Organization-specific workflows

### Roadmap

- **Q1 2025**: Visual workflow designer and advanced scheduling
- **Q2 2025**: Event-driven workflows and ML optimization
- **Q3 2025**: Mobile dashboard and multi-tenant support
- **Q4 2025**: Advanced integrations and enterprise features

---

## 📞 Support & Resources

### Documentation Links

- **[Main README](../../README.md)** - Complete project overview
- **[API Documentation](../../docs/api/README.md)** - Detailed API reference
- **[Deployment Guide](../../DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[Security Guide](../../docs/security/SECURITY_AUDIT.md)** - Security documentation

### Live Platform

- **API Gateway**: https://bhiv-hr-gateway-901a.onrender.com/docs
- **Workflow System**: https://bhiv-hr-gateway-901a.onrender.com/v1/workflows
- **Pipeline Engine**: https://bhiv-hr-gateway-901a.onrender.com/v1/pipelines/templates
- **Endpoint Registry**: https://bhiv-hr-gateway-901a.onrender.com/v1/registry/endpoints

### Contact Information

- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Live Demo**: https://bhiv-hr-gateway-901a.onrender.com
- **Support Email**: support@bhiv-hr.com

---

**BHIV HR Platform v3.2.0** - Complete Workflow & Pipeline Integration System

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: January 18, 2025 | **Status**: 🟢 Production Ready | **Integration**: Complete