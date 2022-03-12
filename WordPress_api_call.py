#!/usr/bin/env python3.10
import requests, json, time, sys, http.client

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def api_call_list(page, headers=headers):
    print(f"page is {page}. headers are {headers}.")
    conn = http.client.HTTPSConnection("nightswithalicecooper.com")
    # conn.request("GET", f'wp-json/wp/v2/posts?_fields=title,link,id&sort=publish_date&categories=4&per_page=100&page={page}')
    conn.request("GET", f"wp-json/wp/v2/posts?_fields=title,link,id&sort=publish_date&categories=4&per_page=1&page={page}")
    r1 = conn.getresponse()

    response = r1.read()
    try:
        data = json.loads(response.decode("utf-8"))
    except:
        print(page)
        print(response)
        sys.exit(str(r1.status) + " " + r1.reason)

    return response, data

def api_call_get(id, headers=headers):
    print(f"id is {id}. headers are {headers}")
    conn = http.client.HTTPSConnection("nightswithalicecooper.com")
    conn.request("GET", f"/wp-json/wp/v2/posts/{id}")
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

    #for number in range(2, int(response.getheaders["X-WP-TotalPages"]) + 1):
    for number in range(2, 3):
        print(response.getheaders)
        print(response.headers)
        response = api_call_list(number)[0]
        for i in response.json():
            data.append(i)
        time.sleep(2)

    return data


def get_post_content(data):
    list = []
    for i in data:
        response = api_call_get(i["id"])
        list.append(response)
        time.sleep(2)

    return list


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


def print_stuff(data):
    print(json.dumps(data, indent=4))


def write_files(list):
    for i in list:
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
                print("non-zero file exists: " + name)



def main():
    data = get_post_list()
    list = get_post_content(data)
    write_files(list)


if __name__ == "__main__":
    main()