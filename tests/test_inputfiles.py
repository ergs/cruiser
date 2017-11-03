from cruiser.inputfiles import InputFile, inparam

def test_params_is_tuple():
    inpfile = InputFile()
    assert isinstance(inpfile.params, tuple)


def test_inputfile_with_inparam():
    class X(InputFile):

        @inparam(default=42.0)
        def a(self, value):
            self.sim['mya'] = value

    x = X()
    assert x.a == 42.0
    assert x.params == ('a',)
    x.a = 28.0
    assert x.a == 28.0
    assert x.sim['mya'] == 28.0
