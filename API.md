# API Documentation

## Base URL
```
https://cognisutra.in/api/v1
```

## Authentication
Most endpoints use session-based authentication. For API access:
1. Login first via `/auth/login`
2. Session cookie will be stored automatically
3. Include cookie in subsequent requests

## Response Format
All API responses follow this format:
```json
{
  "success": true|false,
  "message": "Description",
  "data": {...} or [...],
  "error_code": "ERROR_TYPE" (on error)
}
```

## Rate Limiting
- 30 requests per minute for most endpoints
- 10 requests per minute for admin endpoints
- Rate limit headers included in response

## Endpoints

### Tools

#### Get All Tools
```
GET /tools
```
**Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 20, max: 100) - Items per page
- `category` (string) - Filter by category
- `search` (string) - Search term (min 2 chars)

**Response:**
```json
{
  "success": true,
  "message": "Success",
  "data": [
    {
      "id": "uuid",
      "name": "Tool Name",
      "slug": "tool-name",
      "description": "Description",
      "category": "productivity",
      "price": "₹299/mo",
      "revenue_model": "Freemium"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "pages": 5
  }
}
```

#### Get Single Tool
```
GET /tools/{tool_id}
```
**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Tool Name",
    "slug": "tool-name",
    "description": "Description",
    "long_description": "Longer description",
    "category": "productivity",
    "price": "₹299/mo",
    "revenue_model": "Freemium",
    "features": ["Feature 1", "Feature 2"],
    "tech_stack": ["Flask", "React"],
    "created_at": "2024-01-15T10:30:00Z",
    "bookmarks_count": 42
  }
}
```

#### Create Tool (Admin Only)
```
POST /tools
Authorization: Bearer token
```
**Body:**
```json
{
  "name": "Tool Name",
  "slug": "tool-name",
  "description": "Short description",
  "long_description": "Long description",
  "category": "productivity",
  "price": "₹299/mo",
  "revenue_model": "Freemium",
  "features": ["Feature 1", "Feature 2"],
  "tech_stack": ["Flask", "React"],
  "is_published": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tool created successfully",
  "data": {
    "id": "uuid"
  }
}
```

### Blogs

#### Get All Blogs
```
GET /blogs
```
**Parameters:**
- `page` (int, default: 1)
- `per_page` (int, default: 10, max: 50)
- `category` (string) - Filter by category

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "Blog Title",
      "slug": "blog-title",
      "excerpt": "Short excerpt",
      "category": "tutorial",
      "author": "Author Name",
      "published_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {...}
}
```

#### Get Single Blog
```
GET /blogs/{blog_id}
```
**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Blog Title",
    "slug": "blog-title",
    "content": "<h1>Content</h1><p>Paragraph</p>",
    "excerpt": "Short excerpt",
    "category": "tutorial",
    "author": "Author Name",
    "tags": ["tag1", "tag2"],
    "published_at": "2024-01-15T10:30:00Z"
  }
}
```

### Bookmarks

#### Get User Bookmarks
```
GET /bookmarks
Authentication: Required
```
**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "tool_id": "uuid",
      "tool_name": "Tool Name",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Add Bookmark
```
POST /bookmarks
Authentication: Required
```
**Body:**
```json
{
  "tool_id": "uuid"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Tool bookmarked successfully",
  "data": {
    "id": "uuid"
  }
}
```

#### Remove Bookmark
```
DELETE /bookmarks/{bookmark_id}
Authentication: Required
```
**Response:**
```json
{
  "success": true,
  "message": "Bookmark removed successfully"
}
```

### Statistics

#### Get Public Statistics
```
GET /stats
```
**Response:**
```json
{
  "success": true,
  "data": {
    "total_tools": 100,
    "total_blogs": 50,
    "total_users": 1000,
    "total_bookmarks": 5000
  }
}
```

### Health Check

#### Health Check Endpoint
```
GET /health
```
**Response:**
```json
{
  "success": true,
  "message": "API is running",
  "data": {
    "status": "healthy",
    "version": "1.0"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid input",
  "error_code": "BAD_REQUEST",
  "details": {...}
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Unauthorized",
  "error_code": "UNAUTHORIZED"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Forbidden",
  "error_code": "FORBIDDEN"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Resource not found",
  "error_code": "NOT_FOUND"
}
```

### 409 Conflict
```json
{
  "success": false,
  "message": "Resource already exists",
  "error_code": "CONFLICT"
}
```

### 429 Too Many Requests
```json
{
  "success": false,
  "message": "Rate limit exceeded",
  "error_code": "RATE_LIMIT"
}
```

### 500 Server Error
```json
{
  "success": false,
  "message": "Internal server error",
  "error_code": "SERVER_ERROR"
}
```

## Example Requests

### JavaScript/Fetch
```javascript
// Get tools list
const response = await fetch('https://cognisutra.in/api/v1/tools?page=1&per_page=20');
const data = await response.json();
console.log(data);

// Create tool (admin)
const toolData = {
  name: 'New Tool',
  slug: 'new-tool',
  description: 'Tool description',
  category: 'productivity'
};

const createResponse = await fetch('https://cognisutra.in/api/v1/tools', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include',
  body: JSON.stringify(toolData)
});

const newTool = await createResponse.json();
console.log(newTool);
```

### Python/Requests
```python
import requests

# Get tools
response = requests.get(
    'https://cognisutra.in/api/v1/tools',
    params={'page': 1, 'per_page': 20}
)
data = response.json()
print(data)

# Add bookmark
session = requests.Session()
session.post('https://cognisutra.in/auth/login', data={
    'email': 'user@example.com',
    'password': 'password'
})

bookmark_response = session.post(
    'https://cognisutra.in/api/v1/bookmarks',
    json={'tool_id': 'tool-uuid'}
)
print(bookmark_response.json())
```

### cURL
```bash
# Get tools
curl -X GET 'https://cognisutra.in/api/v1/tools?page=1&per_page=20'

# Get single tool
curl -X GET 'https://cognisutra.in/api/v1/tools/tool-uuid'

# Add bookmark (requires authentication)
curl -X POST 'https://cognisutra.in/api/v1/bookmarks' \
  -H 'Content-Type: application/json' \
  -d '{"tool_id": "tool-uuid"}' \
  -b "session_cookie_here"
```

## Webhooks
Coming soon - Subscribe to events for real-time updates.

## SDKs
Coming soon - Official SDKs for Python, JavaScript, and more.
