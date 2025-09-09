import requests
import json


class PageSpeed:
    API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    DEFAULT_STRATEGY = "mobile"
    VALID_STRATEGIES = {"mobile", "desktop"}
    CATEGORIES = ["performance", "seo", "accessibility", "best-practices"]
    KEY_AUDITS = [
        "first-contentful-paint",
        "largest-contentful-paint",
        "first-meaningful-paint",
        "speed-index",
        "total-blocking-time",
        "cumulative-layout-shift",
        "server-response-time",
    ]

    def __init__(self, url: str, api_key: str, strategy: str = None):
        if not url:
            raise ValueError("URL is required")
        if not api_key:
            raise ValueError("PageSpeed API key is required")

        self.url = self._normalize_url(url)
        self.api_key = api_key
        self.strategy = self._validate_strategy(strategy)

    def _normalize_url(self, url: str) -> str:
        """Ensure URL has proper scheme (https by default)."""
        if not url.startswith(("http://", "https://")):
            return "https://" + url
        return url

    def _validate_strategy(self, strategy: str) -> str:
        """Ensure strategy is either 'mobile' or 'desktop'."""
        if strategy and strategy.lower() in self.VALID_STRATEGIES:
            return strategy.lower()
        return self.DEFAULT_STRATEGY

    def _build_params(self):
        """Build query parameters for the PageSpeed API request."""
        params = [
            ("url", self.url),
            ("key", self.api_key),
            ("strategy", self.strategy),
        ]
        for category in self.CATEGORIES:
            params.append(("category", category))
        return params

    def _parse_audit_data(self, data: dict) -> dict:
        """Extract structured audit results."""
        audit_data = {
            "url": self.url,
            "strategy": self.strategy,
            "loading_experience": data.get("loadingExperience", {}),
            "origin_loading_experience": data.get("originLoadingExperience", {}),
            "lighthouse_result": data.get("lighthouseResult", {}),
            "performance_score": 0,
            "accessibility_score": 0,
            "best_practices_score": 0,
            "seo_score": 0,
            "audits": {},
        }

        # Extract scores
        categories = data.get("lighthouseResult", {}).get("categories", {})
        if isinstance(categories, dict):
            audit_data["performance_score"] = categories.get("performance", {}).get("score", 0) * 100
            audit_data["accessibility_score"] = categories.get("accessibility", {}).get("score", 0) * 100
            audit_data["best_practices_score"] = categories.get("best-practices", {}).get("score", 0) * 100
            audit_data["seo_score"] = categories.get("seo", {}).get("score", 0) * 100

        # Extract key audits
        audits = data.get("lighthouseResult", {}).get("audits", {})
        for audit_key in self.KEY_AUDITS:
            if audit_key in audits:
                audit_data["audits"][audit_key] = audits[audit_key]

        return audit_data

    def audit(self) -> dict:
        """Perform the audit and return structured results as a dictionary."""
        try:
            response = requests.get(self.API_URL, params=self._build_params(), timeout=60)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                return {
                    "success": False,
                    "error": data["error"].get("message", "Unknown API error")
                }

            audit_data = self._parse_audit_data(data)
            return {"success": True, "data": audit_data}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid response from PageSpeed API"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
