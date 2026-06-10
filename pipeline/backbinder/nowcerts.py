"""NowCerts / Momentum AMP API client (first native AMS integration).

Per research/streams/10-ams-feasibility.md: the NowCerts REST API is open to
any agency account with the "API Integration" agent role. Auth is OAuth2
password grant against api.nowcerts.com with the public client id "ngAuthApp".

STATUS: skeleton — endpoints follow the public docs; verify each call against
a sandbox account before first client use. No write path is exposed except
certificate PREP (the agency licensee issues; see launch-plan.md E&O wall).
"""

from __future__ import annotations

from typing import Any

import httpx

BASE_URL = "https://api.nowcerts.com"
CLIENT_ID = "ngAuthApp"


class NowCertsError(RuntimeError):
    pass


class NowCertsClient:
    def __init__(self, username: str, password: str, base_url: str = BASE_URL,
                 http: httpx.Client | None = None):
        self._base = base_url.rstrip("/")
        self._http = http or httpx.Client(timeout=30)
        self._username = username
        self._password = password
        self._token: str | None = None

    # -- auth ---------------------------------------------------------------
    def _authenticate(self) -> None:
        resp = self._http.post(
            f"{self._base}/token",
            data={
                "grant_type": "password",
                "username": self._username,
                "password": self._password,
                "client_id": CLIENT_ID,
            },
        )
        if resp.status_code != 200:
            raise NowCertsError(f"auth failed: {resp.status_code} {resp.text[:200]}")
        self._token = resp.json()["access_token"]

    def _headers(self) -> dict[str, str]:
        if self._token is None:
            self._authenticate()
        return {"Authorization": f"Bearer {self._token}"}

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        resp = self._http.get(f"{self._base}{path}", params=params, headers=self._headers())
        if resp.status_code == 401:
            # token expired — re-auth once
            self._token = None
            resp = self._http.get(f"{self._base}{path}", params=params, headers=self._headers())
        if resp.status_code != 200:
            raise NowCertsError(f"GET {path}: {resp.status_code} {resp.text[:200]}")
        return resp.json()

    # -- reads used by the COI desk and renewal engine ----------------------
    def search_insureds(self, name_fragment: str) -> list[dict[str, Any]]:
        """Find insureds by (partial) name. OData-style filter per public docs."""
        data = self._get(
            "/api/InsuredDetailList",
            params={"$filter": f"contains(commercialName, '{name_fragment}')"},
        )
        return data.get("value", data) if isinstance(data, dict) else data

    def policies_for_insured(self, insured_database_id: str) -> list[dict[str, Any]]:
        data = self._get(
            "/api/PolicyList",
            params={"$filter": f"insuredDatabaseId eq {insured_database_id}"},
        )
        return data.get("value", data) if isinstance(data, dict) else data

    def upcoming_renewals(self, days_ahead: int = 90) -> list[dict[str, Any]]:
        """Policies expiring within the window — feeds the 90/60/30 engine.

        NOTE: filter syntax to be verified against sandbox; some deployments
        expose expirationDate via PolicyList OData.
        """
        data = self._get("/api/PolicyList", params={"$orderby": "expirationDate"})
        return data.get("value", data) if isinstance(data, dict) else data
