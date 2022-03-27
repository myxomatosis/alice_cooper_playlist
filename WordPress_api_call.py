#!/usr/bin/env python3.10
import requests, json, time, sys, http.client, logging

# set up logging to file
logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                                                                    filename='debug.log')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def api_call_list(page, headers=headers):
    if logger.isEnabledFor(logging.DEBUG):
        logging.debug(f"page is {page}. headers are {headers}.")
    conn = http.client.HTTPSConnection("nightswithalicecooper.com")
    if logger.isEnabledFor(logging.DEBUG):
        logging.debug(f'conn.request("GET", f"wp-json/wp/v2/posts?_fields=title,link,id&sort=publish_date&categories=4&per_page=1&page={page}")')
    try:
        conn.request("GET", f"/wp-json/wp/v2/posts?_fields=title,link,id&sort=publish_date&categories=4&per_page=100&page={page}", "", headers)
        r1 = conn.getresponse()
    except ConnectionResetError:
        logging.warning("Connection reset by peer while getting list of posts")
        conn.close()
        time.sleep(2)
        conn.request("GET", f"/wp-json/wp/v2/posts?_fields=title,link,id&sort=publish_date&categories=4&per_page=100&page={page}", "", headers)
        r1 = conn.getresponse()

    response = r1.read()
    try:
        data = json.loads(response.decode("utf-8"))
    except:
        logging.error(f'Page number is {page}')
        logging.error(f'Response for request is: {response}')
        sys.exit(f"r1.status r1.reason")

    return r1, data


def api_call_get(id, headers=headers):
    if logger.isEnabledFor(logging.DEBUG):
        logging.debug(f"id is {id}. headers are {headers}")
    conn = http.client.HTTPSConnection("nightswithalicecooper.com")
    try:
        conn.request("GET", f"/wp-json/wp/v2/posts/{id}", "", headers)
        r1 = conn.getresponse()
    except ConnectionResetError:
        logging.warning("Connection reset by peer while getting post content")
        conn.close()
        time.sleep(3)
        conn.request("GET", f"/wp-json/wp/v2/posts/{id}", "", headers)
        r1 = conn.getresponse()

    response = r1.read()
    try:
        data = json.loads(response.decode("utf-8"))
    except:
        print(id)
        print(response)
        sys.exit(str(r1.status) + " " + r1.reason)

    return data


def get_post_list():
    api_response = api_call_list(1)
    response, data = api_response[0], api_response[1]
    if logger.isEnabledFor(logging.DEBUG):
        logging.debug(f"response is: {response}")
        logging.debug(f"response.getheaders() is: {response.getheaders()}")
        logging.debug(f"response.getheaders()[14] is: {response.getheaders()[14]}")
    for number in range(2, int(response.getheaders()[13][1]) + 1):
        if logger.isEnabledFor(logging.DEBUG):
            logging.debug(f"Running for loop in get_post_list. number is: {number}")
        response = api_call_list(number)[1]
        if logger.isEnabledFor(logging.DEBUG):
            logging.debug(f"response is: {response}\nresponse is type: {type(response)}")
            logging.debug(f"data is: {data}\n data is type: {type(data)}")
        for i in response:
            if logger.isEnabledFor(logging.DEBUG):
                logging.debug(f"i is: {i}\ni is type: {type(i)}")
            data.append(i)
        time.sleep(1)
    return data


def get_post_content(data):
    lst = []
    logging.info(f"Getting post data for {len(data)} posts")
    for i in data:
        response = api_call_get(i["id"])
        lst.append(response)
        time.sleep(1)

    return lst


def is_file_empty_3(file_name):
    """ Check if file is empty by reading first character in it"""
    # open ile in read mode
    with open(file_name, 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
           return True
    return False


def write_files(lst):
    for i in lst:
        name = i["date"].split("-", 1)[0] + "." + i["slug"]
        try:
            f = open("archive/" + name, "x")
            f.write(str(i))
            f.close()
        except FileExistsError:
            if is_file_empty_3("archive/" + name):
                f = open("archive/" + name, "w")
                f.write(str(i))
                f.close()
            else:
                logging.info(f"non-zero file exists: {name}")


def main():
    logging.info("Starting new session")
    logging.info("Running main.data")
    data = get_post_list()
    logging.info("Running main.list")
    lst = get_post_content(data)
    logging.info("Running main.write_files")
    write_files(lst)


if __name__ == "__main__":
    main()
