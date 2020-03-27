import pprint
from googleapiclient.discovery import build  # Import the library
from googleapiclient.errors import HttpError

# api_key = "AIzaSyDA-f7eyKG22-DiVCPjKoRSNVKeMiIc9zY"  # Main key
# api_key = "AIzaSyDmpFiYFOEq9DTIFA1TzxioRj_VywDTnRI"  # Key 2
# api_key = "AIzaSyBQ_scyDxrCV4s-KJi0JZZ45k51fNHyaKM"  # Key 3
api_key = "AIzaSyAJLVJbDhiLPF70W0Y4tjRO66-Wp2DU254"  # Key 4
cse_id = "012244406082711924886:vauyxgi2hjq"
# cse_id = "012244406082711924886:zfvjhom3qgs"
query_service = build("customsearch", "v1", developerKey=api_key)


def google_query(query, api_key, cse_id, **kwargs):
    start = 0
    num = 10
    result_list = []
    try:
        # query_service = build("customsearch", "v1", developerKey=api_key)

        while start < 100:
            query_results = query_service.cse().list(q=query,  # Query
                                                     cx=cse_id,  # CSE ID
                                                     start=start,  # Starting result
                                                     num=num,  # Results per page
                                                     **kwargs  # Other options
                                                     ).execute()
            if 'items' in query_results:
                result_list.extend([j['link'] for j in query_results['items']])
            else:
                return result_list
            start += 10

    except HttpError as e:
        print(e)
        return None

    return result_list


def main():
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
