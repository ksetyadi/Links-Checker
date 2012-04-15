import sys, urllib2

# Get all links related to document(s)
def get_all_links(cnt):
    links = []
    start = 0
    
    # read from the beginning and end of the file
    # until there are no other links
    while True:
        link_tag_pos = cnt.find("<a", start)
        
        # stop reading if there are no other links exists
        if link_tag_pos == -1:
            break
        
        href_pos = cnt.find("href=", link_tag_pos)
        space_pos = cnt.find(" ", href_pos + 6)
        end_tag_pos = cnt.find(">", href_pos + 6)
        
        if space_pos < end_tag_pos:
            pos = space_pos - 1
        else:
            pos = end_tag_pos - 1
        
        link = cnt[href_pos + 6 : pos]
        
        if link not in links:
            if link.find("http") == 0:
                links.append(link)
            
        start = href_pos
        
    return links

# check whether the link is broken or not
def check_broken_link(links):
    print "Found", len(links), "links"
    print ""
    
    # This is for summary
    counter = 0
    up = 0
    broken = 0
    
    for link in links:
        counter = counter + 1
        print "".join([str(counter), ". Checking ", link])
        result = open_url(link)
        
        if result == "error":
            broken = broken + 1
            print "Possibly broken link: ", link
            print ""
        else:
            up = up + 1
            print "Link is up and running"
            print ""
            
    print "Completed."
    print ""
    print "Summary:"
    print "--------"
    print "Total:", len(links), "link(s)"
    print "Up and running:", up, "link(s)"
    print "Possibly broken:", broken, "links(s)"
    print ""
    
# try opening the url and see the response
def open_url(url):
    try:
        #set the timeout to 15 seconds
        # if no response within 15 seconds, the link is probably broken
        result = urllib2.urlopen(url, timeout = 15).read()
    except:
        result = "error"
        
    return result

if __name__ == '__main__':
    args = sys.argv
    
    try:        
        print "Checking links in your site: ", args[1], " ..."
        content = urllib2.urlopen(args[1]).read()
    except:
        print "Something wrong with your connection."
        sys.exit(1)
        
    links = get_all_links(content)
    
    if len(args) == 3 and args[2] == "show":
        print links
    elif len(args) == 2:
        check_broken_link(links)
        