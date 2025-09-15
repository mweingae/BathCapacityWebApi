from datetime import datetime
import logging
import requests

logger = logging.getLogger("app.external_api")

class ExternalAPIClient:
    def __init__(self):
        self.base_url = "https://functions.api.ticos-systems.cloud/api/gates/counter"
        self.timeout = 30

    def fetch_utilization(self, organization_units: list[str]) -> list[dict]:
        """Make API call to fetch current utilization for all facilities."""
        try:
            # Get all facility IDs as comma-separated string
            organization_units_id_string = ",".join(organization_units)
            params = {"organizationUnitIds": organization_units_id_string}

            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            return self._process_response(data)
        
        except Exception as e:
            logger.error(f"Error fetching utilization data: {e}")
            return []

    def _process_response(self, data: list[dict]) -> list[dict]:
        """Process the API response and combine it with facility information from settings."""
        timestamp = datetime.now().isoformat()
        results = []

        for item in data:
            facility_id = str(item.get("organizationUnitId"))
            results.append({
                "facility_id": facility_id,
                "timestamp": timestamp,
                "visitors_count": item.get("personCount", 0),
                "max_capacity": item.get("maxPersonCount", 0)
            })
        
        return results
