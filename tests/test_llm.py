"""Unit tests for LLM integration module."""

import os
import pytest
from unittest.mock import patch, MagicMock

# Import the module under test
from research_assistant.core.llm import (
    LLMClient,
    LLMResponse,
    get_llm_client,
    strip_ansi_codes,
    check_kiro_installed,
)


class TestLLMResponse:
    """Tests for LLMResponse dataclass."""
    
    def test_llm_response_creation(self):
        """Test creating LLMResponse."""
        response = LLMResponse(
            content="Test content",
            model="sonar-pro",
            tokens_used=100,
            success=True,
        )
        assert response.content == "Test content"
        assert response.model == "sonar-pro"
        assert response.tokens_used == 100
        assert response.success is True
        assert response.error is None
        assert response.execution_time_ms == 0
    
    def test_llm_response_with_error(self):
        """Test LLMResponse with error."""
        response = LLMResponse(
            content="",
            model="sonar-pro",
            tokens_used=0,
            success=False,
            error="API error",
            execution_time_ms=100,
        )
        assert response.success is False
        assert response.error == "API error"


class TestStripAnsiCodes:
    """Tests for ANSI code stripping."""
    
    def test_strip_ansi_codes_basic(self):
        """Test stripping basic ANSI codes."""
        text = "\x1b[32mGreen text\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "Green text"
    
    def test_strip_ansi_codes_empty(self):
        """Test with empty string."""
        assert strip_ansi_codes("") == ""
    
    def test_strip_ansi_codes_none(self):
        """Test with None."""
        assert strip_ansi_codes(None) is None


class TestLLMClientProviderDetection:
    """Tests for LLM provider detection."""
    
    def test_detect_perplexity_provider(self):
        """Test Perplexity provider detection."""
        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": "test-key"}, clear=False):
            client = LLMClient()
            assert client._provider == "perplexity"
            assert client.model == "sonar-pro"
    
    def test_detect_no_provider(self):
        """Test no provider available."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('research_assistant.core.llm.check_kiro_installed', return_value=False):
                client = LLMClient()
                assert client._provider == "none"


class TestLLMClientGenerate:
    """Tests for LLM generate method."""
    
    def test_generate_no_provider(self):
        """Test generate with no provider."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('research_assistant.core.llm.check_kiro_installed', return_value=False):
                client = LLMClient()
                response = client.generate("Test prompt")
                assert response.success is False
                assert "No LLM provider" in response.error


class TestLLMClientPerplexity:
    """Tests for Perplexity API integration."""
    
    @patch('urllib.request.urlopen')
    def test_perplexity_success(self, mock_urlopen):
        """Test successful Perplexity API call."""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"choices":[{"message":{"content":"Test response"}}],"usage":{"total_tokens":50}}'
        mock_response.__enter__ = lambda s: mock_response
        mock_response.__exit__ = MagicMock()
        mock_urlopen.return_value = mock_response
        
        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": "test-key"}, clear=False):
            client = LLMClient()
            response = client.generate("Test prompt")
            assert response.success is True
            assert response.content == "Test response"
            assert response.tokens_used == 50


class TestNoHardcodedSecrets:
    """Tests to ensure no hardcoded secrets."""
    
    def test_no_hardcoded_api_keys(self):
        """Verify no API keys in source code."""
        import research_assistant.core.llm as llm_module
        import inspect
        source = inspect.getsource(llm_module)
        
        # Check for common API key patterns
        assert "pplx-" not in source
        assert "sk-ant-" not in source
        assert "sk-proj-" not in source


class TestGetLLMClientSingleton:
    """Tests for singleton pattern."""
    
    def test_singleton_returns_same_instance(self):
        """Test that get_llm_client returns same instance."""
        # Reset singleton
        import research_assistant.core.llm as llm_module
        llm_module._llm_client = None
        
        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": "test-key"}, clear=False):
            client1 = get_llm_client()
            client2 = get_llm_client()
            assert client1 is client2
