from urllib.request import urlopen

class Locations(object):
    '''
    Find locations of the datasets from the download area because the download links are hashes and cannot be predicted

    input:
        starting URI "data-sets-available-for-download' (currently-published location of the RRC data for download)
    output:

        Structure of parsed object:
            DataSetIndex:
                list of DatasetType

            DatasetType: e.g. data_type: "Production Data"
                contains Dataset list

            Dataset:
                dataset_name: Dataset-name: e.g. "Gas Ledger Dist 1,2,3"
                download_uri: e.g. https://mft.rrc.texas.gov/link/c45ee840-9d50-4a74-b6b0-dba0cb4954b7
                manual_uri: (for the COBOL copy book) e.g. https://www.rrc.texas.gov/media/jukdy4oh/gsa020k.pdf
                update_schedule: e.g. Monthly Available by the 20th
                detail_uri: e.g. https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/#gas-masters

    Approach: parse starting_uri with beautiful soup, index each of the 'heading' values, make a list of each of the data sets under that heading
    with the "dataset_name", "download_uri",  "manual_uri", "update_schedule" and "details_uri"

    Sample HTML as of May 16, 2024:

    '''

    def __init__(self, starting_url):
        self.starting_url = starting_url
        page = urlopen(starting_url)
        dataset_download_html = page.read()
        dataset_start_html = dataset_download_html.decode("utf-8")
        import pdb; pdb.set_trace()
