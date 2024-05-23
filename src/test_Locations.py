from Locations import Locations

def test_locations():

    html_page = Locations('https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/')
    # read location
    # parse out datasets
    # get the dataset URL
    # parse the dataset files under dataset URL
    assert(html_page.h1[0] == 'Data Sets Available for Download')
    assert(html_page.h2[1] == 'Data Sets')


