import requests
from typing import Any

BASE_URL = "https://lookup.kulturpool.ai"

def get_entity(qid: str) -> dict[str, Any]:
    """Fetch entity details for a Wikidata QID."""
    response = requests.get(
        f"{BASE_URL}/api/entities/{qid}",
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("API returned an unexpected entity response")

    return data


def query_api(search_query: str) -> Any:
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={"query": search_query},
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_record(record_id_link: str):
    response = requests.get(
        f"{BASE_URL}/api/records/{record_id_link}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def parse_record_aggregated_cho(record_api_response: dict[str, Any]) -> dict[str, Any]:
    """Extract the aggregatedCHO object from the record details API response."""
    original_record = record_api_response.get("original_record", {})
    aggregated_cho = original_record.get("aggregatedCHO", {})
    
    return aggregated_cho

def extract_qids_from_json(api_response: dict[str, Any], limit: int) -> list[str]:
    """Extract up to the first 5 QIDs from the search API response."""
    results = api_response.get("results", [])
    
    # Extract the 'q_id' from the first 5 records (or fewer if less than 5 exist)
    qids = []
    for record in results[:limit]:
        qid = record.get("q_id")
        if qid:
            qids.append(qid)
            
    return qids


def parse_entity_data(api_response: dict[str, Any], limit: int) -> dict[str, Any]:
    """Extract English label, English description, and the first 5 record IDs."""
    label_en = api_response.get("label_en")
    description_en = api_response.get("description_en")
    entity_types = api_response.get("entity_type", [])
    
    # Get all record IDs and slice the first 5
    all_record_ids = api_response.get("record_ids", [])
    first_five_records = all_record_ids[:limit]
    
    return {
        "label_en": label_en,
        "description_en": description_en,
        "record_ids": first_five_records,
        "entity_type": entity_types,
    }


#https://lookup.kulturpool.ai/api/entities/Q254
def get_entity(qid: str):
    response = requests.get(
        f"{BASE_URL}/api/entities/{qid}",
        #params={},
        timeout=30,
    )
    response.raise_for_status()

    return response.json()



def main():
    
    search_query = input("Search for: ").strip()
    if not search_query:
        raise ValueError("Search text cannot be empty")

    results = query_api(search_query)
    #print(results)
    first_five_qids = extract_qids_from_json(results, limit = 5)
    print("First 5 QIDs:", first_five_qids)
    
    first_ten_qids = extract_qids_from_json(results, limit=10)
    print(f"Top 10 QIDs found: {first_ten_qids}\n")
    
    for qid in first_ten_qids:
        print(f"Fetching entity data for {qid}...")
        try:
            entity_data = get_entity(qid)
            parsed_entity_results = parse_entity_data(entity_data, limit=5)
            print(parsed_entity_results)
            print("-" * 40)
        except requests.exceptions.HTTPError as e:
            print(f"Skipping {qid}: Entity not found on server (HTTP {e.response.status_code})")
        except Exception as e:
            print(f"An error occurred for {qid}: {e}")
    
    record_id = input("URL (record id): ").strip()
    
    if not search_query:
        raise ValueError("Cannot be empty")

    record_results = get_record(record_id)
    print(record_results)
    
    
if __name__ == '__main__':
    main()