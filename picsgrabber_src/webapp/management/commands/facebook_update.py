# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime, timedelta
from django.core.management import call_command
from django.core.management.base import BaseCommand
import requests.packages.urllib3
import json
import logging
import facebook
from webapp.models import Grabber
import urllib2
from django.conf import settings

# Disable usrllib warnings for better look console output.
requests.packages.urllib3.disable_warnings()
logger = logging.getLogger("commands")


def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    # Get page token to post as the page. You can skip
    # the following if you want to post as yourself.
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Handle the Verbosity level
        verbosity = options.get('verbosity')
        if verbosity == 0:
            logging.getLogger('commands').setLevel(logging.WARN)
        elif verbosity == 1:  # default
            logging.getLogger('commands').setLevel(logging.INFO)
        elif verbosity > 1:
            logging.getLogger('commands').setLevel(logging.DEBUG)
        if verbosity > 2:
            logging.getLogger().setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        logger.addHandler(ch)
        # Start with testing for lock files, and provide a mechanism to
        if os.access(os.path.expanduser("~/.lockfile.facebook.lock"), os.F_OK):
            pidfile = open(os.path.expanduser("~/.lockfile.facebook.lock"), "r")
            pidfile.seek(0)
            old_pd = pidfile.readline()

            if os.path.exists("/proc/%s" % old_pd):
                print "You already have an instance of the program running"
                print "It is running as process %s," % old_pd
                sys.exit(1)
            else:
                print "File is there but the program is not running"
                print "Removing lock file for the: %s as it can be there" \
                    " because of the program last time it was run" % old_pd
                os.remove(os.path.expanduser("~/.lockfile.facebook.lock"))

        # This is part of code where we put a PID file in the lock file
        pidfile = open(os.path.expanduser("~/.lockfile.facebook.lock"), "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close

        # Start logging
        startTime = datetime.now()
        logger.info("Program Start: %s", startTime)
        keys = {
            # Test Page
            "page_id": getattr(settings, 'FB_PAGE_ID', ''),
            "access_token": getattr(settings, 'FB_PAGE_TOKEN', '')
        }
        try:
            api = get_api(keys)
            logger.info("Making API call to facebook")
        except Exception, e:
            logger.info("Error while making API calls to Facebook: %s", e)
            os.remove(os.path.expanduser("~/.lockfile.facebook.lock"))
            sys.exit(1)

        # Link to Imgur GIFs
        item = Grabber.objects.first()
        extension = item.url.split(".")[-1]
        logger.info("Extension found in URL: %s", extension)
        file_name = "temp_files/" + item.url.split("/")[-1]
        added_text = "\n ---- \n PS: Don't forget to like our page! 👍👍  "
        # msg = item.description + "\n\n Don't forget to follow us! "
        msg = item.description.encode('utf-8') + added_text

        if extension == "gif" or extension == "mp4":
            # We need to upload a link to Gif or MP4.

            attachment = {
                'name': 'Name',
                'link': item.url,
                # 'caption': 'Check out this example',
                # 'description': 'This is a longer description of the attachment',
                'picture': item.url
            }
            logger.info("Attachments requested: %s", json.dumps(attachment, indent=1))
            status = api.put_wall_post(msg, attachment=attachment)
            item.delete()
            logger.info(status)
        else:
            # Work with other type of images

            logger.info("Trying to dowload: %s into: %s", item.url, file_name)
            try:
                u = urllib2.urlopen(item.url)
                localfile = open(file_name, 'w')
                localfile.write(u.read())
                localfile.close()
            except Exception, e:
                logger.info("Error while downloading file: %s", e)
                os.remove(os.path.expanduser("~/.lockfile.facebook.lock"))
                sys.exit(1)
            status = api.put_photo(image=open(file_name, 'rb',), caption=msg)
            logger.info(status)
            os.remove(file_name)
            item.delete()
        # Remove lock file
        os.remove(os.path.expanduser("~/.lockfile.facebook.lock"))
