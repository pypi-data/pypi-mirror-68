from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

import requests


SLIDO_API_URL_BASE = "https://app.sli.do/api/v0.5/"


class SlidoClient:
    def __init__(
        self, event_hash: str, auth_token: str, api_base: Optional[str] = None
    ):
        if api_base is None:
            self.api_base = SLIDO_API_URL_BASE
        else:
            self.api_base = api_base

        self.session = self._create_session(auth_token)
        self.event_uuid, self.event_id, self.event_section_id = self._get_event_data(
            event_hash
        )

    def _create_session(self, token: str) -> requests.Session:
        session = requests.Session()
        session.headers["authorization"] = f"Bearer {token}"
        return session

    def _get_event_data(self, event_hash: str) -> Tuple[str, int, int]:
        event_uuid = self.session.get(
            self.api_base + "events", params={"hash": event_hash},
        ).json()[0]["uuid"]
        event_data = self.session.get(self.api_base + f"events/{event_uuid}",).json()
        event_id = event_data["event_id"]
        event_section_id = event_data["sections"][0]["event_section_id"]
        return event_uuid, event_id, event_section_id

    def send_question(self, text: str) -> Dict[str, Any]:
        response = self.session.post(
            self.api_base + f"/events/{self.event_uuid}/questions",
            json={
                "event_id": self.event_id,
                "event_section_id": self.event_section_id,
                "is_anonymous": True,
                "labels": [],
                "media_ids": [],
                "path": "/questions",
                "text": text,
            },
        )
        response.raise_for_status()
        return response.json()
