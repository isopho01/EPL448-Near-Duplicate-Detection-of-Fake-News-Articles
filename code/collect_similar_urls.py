import pprint
from googleapiclient.discovery import build  # Import the library
from googleapiclient.errors import HttpError


def google_query(query, api_key, cse_id, start=0, num=10, **kwargs):
    result_list = []
    query_service = build("customsearch", "v1", developerKey=api_key)

    # Get only last few
    if (start + num - 1) >= 100:
        num = 100 - start

    # Loop until limit is reached
    while (start + num - 1) < 100:
        try:
            query_results = query_service.cse().list(q=query,  # Query
                                                     cx=cse_id,  # CSE ID
                                                     start=start,  # Starting result
                                                     num=num,  # Results per page
                                                     **kwargs  # Other options
                                                     ).execute()

            result_list.extend(query_results['items'])
        except HttpError as e:
            print(e)
            return result_list  # Return gathered results

        start = start + num

        # Get only last few
        if (start + num - 1) >= 100:
            num = 100 - start

    return result_list


def main():
    # api_key = "AIzaSyDA-f7eyKG22-DiVCPjKoRSNVKeMiIc9zY" # Main key
    # api_key = "AIzaSyDmpFiYFOEq9DTIFA1TzxioRj_VywDTnRI" # Key 2
    api_key = "AIzaSyBQ_scyDxrCV4s-KJi0JZZ45k51fNHyaKM"  # Key 3
    cse_id = "012244406082711924886:vauyxgi2hjq"

    my_results_list = []
    my_results = google_query("Did Miley Cyrus and Liam Hemsworth secretly get married?",
                              api_key,
                              cse_id,
                              start=0,
                              num=10,
                              )
    for result in my_results:
        my_results_list.append(result['link'])

    pprint.pprint(my_results_list)
    print(len(my_results_list))


if __name__ == '__main__':

    main()