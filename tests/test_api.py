"""
Tests for API endpoints
"""

import pytest
from tests.conftest import assert_response_ok, assert_response_created, assert_response_not_found

class TestToolsAPI:
    """Test tools API endpoints"""
    
    def test_get_tools_list(self, api_helper, sample_tool):
        """Test getting tools list"""
        data = api_helper.get_json('/api/v1/tools')
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_tools_with_pagination(self, api_helper, sample_tool):
        """Test getting tools with pagination"""
        data = api_helper.get_json('/api/v1/tools?page=1&per_page=10')
        assert data['success'] is True
        assert 'pagination' in data
    
    def test_get_single_tool(self, api_helper, sample_tool):
        """Test getting single tool"""
        tool_id = sample_tool.id
        data = api_helper.get_json(f'/api/v1/tools/{tool_id}')
        assert data['success'] is True
        assert data['data']['id'] == str(tool_id)
    
    def test_get_nonexistent_tool(self, api_helper):
        """Test getting nonexistent tool"""
        data = api_helper.get_json('/api/v1/tools/nonexistent-id')
        assert data['success'] is False

class TestBlogsAPI:
    """Test blogs API endpoints"""
    
    def test_get_blogs_list(self, api_helper, sample_blog):
        """Test getting blogs list"""
        data = api_helper.get_json('/api/v1/blogs')
        assert data['success'] is True
        assert isinstance(data['data'], list)
    
    def test_get_single_blog(self, api_helper, sample_blog):
        """Test getting single blog"""
        blog_id = sample_blog.id
        data = api_helper.get_json(f'/api/v1/blogs/{blog_id}')
        assert data['success'] is True
        assert data['data']['id'] == str(blog_id)

class TestStatsAPI:
    """Test statistics API"""
    
    def test_get_stats(self, api_helper, sample_tool, sample_blog):
        """Test getting statistics"""
        data = api_helper.get_json('/api/v1/stats')
        assert data['success'] is True
        assert 'total_tools' in data['data']
        assert 'total_blogs' in data['data']
        assert 'total_users' in data['data']

class TestHealthAPI:
    """Test health check endpoint"""
    
    def test_health_check(self, api_helper):
        """Test health check"""
        data = api_helper.get_json('/api/v1/health')
        assert data['success'] is True
        assert data['data']['status'] == 'healthy'
