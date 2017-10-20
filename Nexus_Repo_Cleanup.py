import xml.etree.ElementTree as ET
import os
import httplib
import datetime
import string
import base64
import getpass

NEXUSHOST = "projects.itemis.de"
USE_SSL = True
NEXUSREPOSITORY = "mbeddr.core"
NEXUSBASEURL = "/nexus/service/local/repositories/"

NEXUSUSER=os.environ['nexusUsername']
NEXUSPASS=os.environ['nexusPassword']
ARTIFACTGROUP ="com.mbeddr"
ARTIFACTNAME = "platform"  # can be an artifact ID or None. None first searches for artifacts in the group
ARTIFACTMAXLASTMODIFIED = datetime.datetime.strptime("2017-10-20 12:00:00","%Y-%m-%d %H:%M:%S")
ARTIFACTMINLASTMODIFIED = datetime.datetime.strptime("2017-10-19 12:00:00","%Y-%m-%d %H:%M:%S")

# generates URL based on constants and artifactname, calls Nexus and returns an ElementTree
def get_nexus_artifact_version_listing(artifactname):
    if (USE_SSL):
        conn = httplib.HTTPSConnection(NEXUSHOST)
    else:
        conn = httplib.HTTPConnection(NEXUSHOST)

    userAndPass = string.strip(base64.encodestring(NEXUSUSERNAME + ':' + NEXUSPASSWORD))
    headers = {'Authorization': 'Basic %s' % userAndPass}

    url = NEXUSBASEURL + NEXUSREPOSITORY + "/content/" + ARTIFACTGROUP.replace(".", "/") + "/" + artifactname + "/"
    #print "URL to determine artifact versions: "+""+NEXUSHOST+url
    conn.request("GET", url, headers=headers)
    response = conn.getresponse()
    if (response.status == 200):
        return ET.fromstring(response.read())
    else:
        print "error: ", response.status
        return None


# generates URL based on constants, calls Nexus and returns an ElementTree
def get_nexus_artifact_names():
    if (USE_SSL):
        conn = httplib.HTTPSConnection(NEXUSHOST)
    else:
        conn = httplib.HTTPConnection(NEXUSHOST)

    userAndPass = string.strip(base64.encodestring(NEXUSUSERNAME + ':' + NEXUSPASSWORD))
    headers = {'Authorization': 'Basic %s' % userAndPass}
    url = NEXUSBASEURL + NEXUSREPOSITORY + "/content/" + ARTIFACTGROUP.replace(".", "/") + "/"
    conn.request("GET", url, headers=headers)
    response = conn.getresponse()
    if (response.status == 200):
        return ET.fromstring(response.read())
    else:
        print "error: ", response.status
        return None

def content_item_in_selection(content_item):
    relativePath = content_item.find("./relativePath").text
    lastmodified = content_item.find("./lastModified").text
    leaf = content_item.find("./leaf").text
    lastmodified_short = lastmodified[0:19]
    try:
        lastmodified_dt = datetime.datetime.strptime(lastmodified_short, "%Y-%m-%d %H:%M:%S")
    except:
        print "Unable to parse " + lastmodified
        raise

    if (leaf == "false"):
        if (
                    ((
                             ARTIFACTMINLASTMODIFIED is not None and lastmodified_dt >= ARTIFACTMINLASTMODIFIED) or ARTIFACTMINLASTMODIFIED is None)
                and ((
                             ARTIFACTMAXLASTMODIFIED is not None and lastmodified_dt <= ARTIFACTMAXLASTMODIFIED) or ARTIFACTMAXLASTMODIFIED is None)
        ):
            lastmodified_in_selection = True
        else:
            lastmodified_in_selection = False
        if (lastmodified_in_selection):
            return True
        else:
            return False
    else:
        return False


def remove_artifact(groupid, artifactid, version):
    print "Artifact to be removed " + groupid + ": " + artifactid + ": " + version
    url = NEXUSBASEURL + NEXUSREPOSITORY + "/content/" + groupid.replace(".", "/") + "/" + artifactid + "/" + version
    auth = string.strip(base64.encodestring(NEXUSUSERNAME + ':' + NEXUSPASSWORD))
    if (USE_SSL):
        service = httplib.HTTPS(NEXUSHOST)
    else:
        service = httplib.HTTP(NEXUSHOST)

    service.putrequest("DELETE", url)
    service.putheader("Host", NEXUSHOST)
    service.putheader("User-Agent", "Python http auth")
    service.putheader("Content-type", "text/html; charset=\"UTF-8\"")
    service.putheader("Authorization", "Basic %s" % auth)
    service.endheaders()
    service.send("")
    statuscode, statusmessage, header = service.getreply()

    print "Response: ", statuscode, statusmessage
    print "Headers: ", header
    res = service.getfile().read()
    print 'Content: ', res

def remove_artifacts_from_nexus():
    if (ARTIFACTNAME is not None):
        artifact_versions = get_nexus_artifact_version_listing(ARTIFACTNAME)
        content_items = artifact_versions.findall('./data/content-item')
        for content_item in content_items:
            if content_item_in_selection(content_item):
                #print "to remove: " + content_item.find("./text").text
                str = content_item.find("./text").text
                if (str.startswith('milestone')) :
                    print
                else:
                    print "Removing artifacts"+ content_item.find("./text").text
                    #remove_artifact(ARTIFACTGROUP, ARTIFACTNAME, content_item.find("./text").text)
    else:
        artifact_names = get_nexus_artifact_names()
        for artifact_name in artifact_names.findall("./data/content-item"):
            artifactname = artifact_name.find("./text").text
            artifact_versions = get_nexus_artifact_version_listing(artifactname)
            content_items = artifact_versions.findall('./data/content-item')
            for content_item in content_items:
                if content_item_in_selection(content_item):
                    #print "to remove: " + content_item.find("./text").text
                    str=content_item.find("./text").text
                    #print str.startswith('milestone')
                    str = content_item.find("./text").text
                    if (str.startswith('milestone')):
                        print
                    else:
                        print "Removing artifacts" + content_item.find("./text").text
                        #remove_artifact(ARTIFACTGROUP, artifactname, content_item.find("./text").text)

NEXUSUSERNAME = NEXUSUSER
NEXUSPASSWORD = NEXUSPASS
remove_artifacts_from_nexus()