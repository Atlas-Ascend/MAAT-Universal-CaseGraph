import pytest

from maat.agent import AgentUnavailableError, agent_runtime_configured, build_agent


def test_agent_runtime_is_explicit_when_credentials_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "AWS_ACCESS_KEY_ID",
        "AWS_PROFILE",
        "AWS_WEB_IDENTITY_TOKEN_FILE",
        "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",
        "AWS_CONTAINER_CREDENTIALS_FULL_URI",
    ):
        monkeypatch.delenv(name, raising=False)

    assert agent_runtime_configured() is False
    with pytest.raises(AgentUnavailableError):
        build_agent()
