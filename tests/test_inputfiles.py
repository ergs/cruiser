from cruiser.inputfiles import InputFile

def test_params_is_tuple():
    inpfile = InputFile()
    assert isinstance(inpfile, tuple)