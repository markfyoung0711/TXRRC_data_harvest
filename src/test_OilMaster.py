from OilMaster import OilMaster

def test_OilMaster():
    data_division_file = 'ola_copybook.txt'
    data_division_file = 'a.txt'
    data_division_file = 'b.txt'
    data_division_file = 'o.txt'
    om = OilMaster(data_division_file)

    assert(om.get_format() is not None)
