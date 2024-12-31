from typing import Tuple
from uuid import uuid4

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.test import AsyncClient


@pytest.fixture
async def create_user(django_user_model):
    """테스트용 사용자를 생성합니다.

    Returns:
        User: 생성된 사용자 객체를 반환합니다.
    """
    username = f"testuser_{uuid4().hex[:8]}"  # 랜덤 사용자명 생성
    user = await django_user_model.objects.acreate(username=username)
    return user


@pytest.fixture
async def auth_credentials(create_user) -> tuple[str, str]:
    """인증된 사용자의 자격증명을 생성합니다.

    Returns:
        tuple[str, str]: (username, session_key) 튜플을 반환합니다.
    """

    session = SessionStore()
    session[SESSION_KEY] = str(create_user.pk)
    session[BACKEND_SESSION_KEY] = "django.contrib.auth.backends.ModelBackend"
    session[HASH_SESSION_KEY] = create_user.get_session_auth_hash()
    await sync_to_async(session.save)()

    return create_user.username, session.session_key


@pytest.fixture
def csrf_async_client() -> AsyncClient:
    """CSRF 검증이 활성화된 AsyncClient fixture"""
    return AsyncClient(enforce_csrf_checks=True)
