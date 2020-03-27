import pprint
from googleapiclient.discovery import build  # Import the library
from googleapiclient.errors import HttpError


def google_query(query, api_key, cse_id, start=0, num=10, **kwargs):
    try:
        query_service = build("customsearch", "v1", developerKey=api_key)

        query_results = query_service.cse().list(q=query,  # Query
                                                 cx=cse_id,  # CSE ID
                                                 start=start,  # Starting result
                                                 num=num,  # Results per page
                                                 **kwargs  # Other options
                                                 ).execute()
        return [j['link'] for j in query_results['items']]

    except HttpError as e:
        print(e)
        return None


def main():
    # api_key = "AIzaSyDA-f7eyKG22-DiVCPjKoRSNVKeMiIc9zY" # Main key
    api_key = "AIzaSyDmpFiYFOEq9DTIFA1TzxioRj_VywDTnRI" # Key 2
    # api_key = "AIzaSyBQ_scyDxrCV4s-KJi0JZZ45k51fNHyaKM"  # Key 3
    cse_id = "012244406082711924886:vauyxgi2hjq"

    i = 0
    while google_query("Did Miley Cyrus and Liam Hemsworth secretly get married?",
                       api_key,
                       cse_id,
                       ) is not None:
        i = i + 1
        print(i)


# for result in my_results:
#     pprint.pprint(result)


if __name__ == '__main__':
    main()
