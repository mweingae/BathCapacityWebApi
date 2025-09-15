from app.services.external_api import ExternalAPIClient
import asyncio
from sqlmodel import Session, select
from app.models import Data, Facility, Settings
import logging
from app.database import get_session

logger = logging.getLogger("app.services.data_collector")

class DataCollector:
    def __init__(self):
        self.api_client = ExternalAPIClient()
        self.is_running = False

    async def run_continuous_collection(self):
        """Main background loop"""
        self.is_running = True
        logger.info("Starting continuous data collection...")
        
        while self.is_running:
            try:
                db = next(get_session())

                settings = self.get_settings(db)
                if not settings:
                    raise Exception("No settings in db")
                self.api_client.timeout = settings.external_api_timeout

                facilities = self.get_facilites(db)
                if not facilities:
                    raise Exception("No facilities in db")
                facility_ids = [facility.organization_unit for facility in facilities]

                # Fetch new data
                new_data = self.api_client.fetch_utilization(facility_ids)
            
                if new_data:
                    # Swap organization unit ID with facility ID
                    self.replace_facility_id(new_data, facilities)

                    # Store in database
                    self.store_data_batch(new_data, db)
                    logger.info(f"Stored {len(new_data)} new records")

                await asyncio.sleep(settings.fetch_interval)

            except Exception as e:
                logger.error(f"Error in data collection: {e}")
                await asyncio.sleep(60)  # Wait a minute before retry
                
            finally:
                if 'db' in locals():
                    db.close()

    def get_settings(self, db: Session) -> Settings | None:
        return db.exec(select(Settings)).first()

    def get_facilites(self, db: Session) -> list[Facility] | None:
        results = db.exec(select(Facility))
        if results:
            return list(results)
        else:
            return None
    
    def replace_facility_id(self, data, facilities: list[Facility]):
        for item in data:
            facility_match = list(filter(lambda facility: facility.organization_unit == item["facility_id"], facilities))
            item["facility_id"] = facility_match[0].id
        
    def store_data_batch(self, data_batch: list[dict], db: Session):
        """Efficiently store batch of data"""
        
        for item in data_batch:
            entry = Data(
                timestamp=item["timestamp"],
                visitors_count=item["visitors_count"],
                max_capacity=item["max_capacity"],
                facility_id=item["facility_id"])
            
            db.add(entry)
            db.commit()
    
    def stop_collection(self):
        """Stop the collection loop"""
        self.is_running = False