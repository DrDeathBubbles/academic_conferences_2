#!/usr/bin/env python3

import time
import requests
import os
import sys
import csv
import errno
import json
import queue
import codecs
from collections import defaultdict
from urllib import parse


try:
    #FC_API_KEY = os.environ['FC_API_KEY']
    FC_API_KEY="2a8d7aedf27b2aa8"
except KeyError:
    print("Set FC_API_KEY environment variable before running")
    raise SystemExit

FC_OUTDIR = "full_contact_responses"
FC_URLS = {
    'company': (
        "https://api.fullcontact.com/v2/company/lookup.json"
        "?domain={}"
        "&apiKey={}"
        "&keyPeople=true"
    ),
    'person': (
        "https://api.fullcontact.com/v2/person.json"
        "?email={}"
        "&apiKey={}"
    )
}


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def load_companies(csv_file, column='url'):
    company_urls = set()
    with open(csv_file) as cin:
        for row in csv.DictReader(cin):
            parsed_url = parse.urlparse(row.get(column))
            c_url = parsed_url.netloc
            if not c_url:
                c_url = parsed_url.path
            if c_url:
                if c_url.startswith('www.'):
                    # drop the www.
                    c_url = c_url[4:]
                if len(c_url):
                    company_urls.add(c_url)
    return list(company_urls)


def load_emails(csv_file, column='email'):
    emails = set()
    with open(csv_file, ) as cin:
        for idx, row in enumerate(
                csv.DictReader(cin)):
            emails.add(row.get(column))
    print(len(list(emails)))
    return list(emails)


def save_response(cleaned_url, json_reponse):
    out_dir = os.path.join(FC_OUTDIR, cleaned_url[:2])
    mkdir_p(out_dir)
    out_fname = os.path.join(out_dir, cleaned_url) + ".json"
    with open(out_fname, 'w') as jout:
        json.dump(json_reponse, jout, indent=2)


def get_fullcontact(urls, request_type):
    request_queue = queue.Queue()
    times_seen = defaultdict(int)
    for url in urls:
        request_queue.put(url)
    still_working = True
    c_url = None
    while still_working:
        try:
            c_url = request_queue.get_nowait()
            times_seen[c_url] += 1
            print("Working on {} (attempt {})"
                  .format(c_url, times_seen[c_url]))
            request_url = FC_URLS[request_type].format(
                c_url, FC_API_KEY)
            print(request_url)
            response = requests.get(request_url)
            if response.status_code in [200, '200']:
                save_response(c_url, response.json())
            elif response.status_code in [202, '202']:
                # The query exists, we must try again
                request_queue.put(c_url)
            elif response.status_code in [404, '404']:
                print("No record for {}".format(c_url))
            else:
                print("Got {} for {}".format(
                    response.status_code, c_url))
        except TypeError:
            request_queue.put(c_url)
        except queue.Empty:
            still_working = False

        # Exponential backoff
        time.sleep(
            2 ** (times_seen.get(c_url, 1) - 1) * 1.01 *
            float(int(response.headers['x-rate-limit-reset'])) /
            int(response.headers['x-rate-limit-limit']))


def filter_existing_responses(urls):
    filtered_urls = []
    for url in urls:
        expected_path = os.path.join(FC_OUTDIR, url[:2], url) + ".json"
        if not os.path.exists(expected_path):
            filtered_urls.append(url)
    return filtered_urls


if __name__ == "__main__":
    try:
        csv_file = sys.argv[1]
        request_type = sys.argv[2]
        csv_column = sys.argv[3]
    except IndexError:
        raise SystemExit(
            "Usage: full_contact.py INPUT_FILE TYPE COLUMN_NAME"
        )

    if request_type == "company":
        to_get = load_companies(csv_file, column=csv_column)
    elif request_type == "person":
        to_get = load_emails(csv_file, column=csv_column)
    else:
        raise SystemExit("Valid types: company, person")
    get_fullcontact(
        filter_existing_responses(to_get),
        request_type=request_type)