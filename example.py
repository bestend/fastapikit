import os

import uvicorn
from fastapi import FastAPI

from api import router as apiv1
from app_config import AppConfig
from fastapi_kit import create_app
from services.grafana.webhook_service import GrafanaWebhookService
from services.works import WorksNotificationService
from services.works.api_client import WorksApiClient

if os.environ.get("PYCHARM_REMOTE_DEBUG"):
    import pydevd_pycharm


def attach(config: AppConfig):
    if os.environ.get("PYCHARM_REMOTE_DEBUG"):
        print("Connecting to debugger...")
        pydevd_pycharm.settrace(
            "0.0.0.0",
            port=config.pycharm_debug_port,
            stdoutToServer=True,
            stderrToServer=True,
        )


def build() -> tuple[AppConfig, FastAPI]:
    # 환경변수 CONFIG_FILE에서 설정 파일 경로 읽기 (기본값: config.yaml)
    config_file = os.environ.get("CONFIG_FILE", "config.yaml")

    config = AppConfig.load(config_file=config_file, source_order=["env", "file"])

    attach(config)

    async def startup_coroutine(app: FastAPI):
        # Works API 클라이언트 초기화
        api_client = WorksApiClient(
            server_id=config.works_server_id,
            consumer_key=config.works_consumer_key,
            private_key=config.works_private_key,
            token_file=config.token_file,
            api_id=config.works_api_id,
            bot_no=config.works_bot_no,
        )

        # Works 알림 서비스 초기화
        works_notification_service = WorksNotificationService(api_client=api_client)

        # Grafana Webhook 서비스 초기화
        grafana_webhook_service = GrafanaWebhookService(
            works_notification_service=works_notification_service,
        )

        # app.state에 서비스 저장
        app.state.grafana_webhook_service = grafana_webhook_service

    app = create_app(
        [apiv1],
        title=config.title,
        version=config.version,
        prefix_url=config.prefix_url,
        graceful_timeout=config.graceful_timeout,
        docs_enable=config.docs_enable,
        docs_prefix_url=config.docs_prefix_url,
        middlewares=[],
        dependencies=[],
        startup_coroutines=[startup_coroutine],
        shutdown_coroutines=[],
        health_check_api="/healthz",
        add_external_basic_auth=config.add_external_basic_auth,
    )

    return config, app


if __name__ == "__main__":
    config, app = build()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.port,
        log_level=config.log_level.lower(),
        limit_concurrency=config.limit_concurrency if config.limit_concurrency > 0 else None,
    )
else:
    config, app = build()
