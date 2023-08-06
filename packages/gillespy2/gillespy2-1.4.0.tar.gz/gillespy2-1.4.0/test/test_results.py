import unittest
import os
import tempfile
from gillespy2.core import Model, Species, Reaction, Parameter
from gillespy2.core.results import Results, Trajectory

class TestResults(unittest.TestCase):

    def test_pickle_stable_plot_iterate(self):
        from unittest import mock
        from gillespy2.core.results import _plot_iterate
        trajectory = Trajectory(data={'time':[0.],'foo':[1.]}, model=Model('test_model'))
        import pickle
        trajectory_unpickled = pickle.loads(pickle.dumps(trajectory))
        import matplotlib
        with mock.patch('matplotlib.pyplot.plot') as mock_method_before_pickle:
            _plot_iterate(trajectory)
        with mock.patch('matplotlib.pyplot.plot') as mock_method_after_pickle:
            _plot_iterate(trajectory_unpickled)
        assert mock_method_before_pickle.call_args_list == mock_method_after_pickle.call_args_list

    def test_pickle_stable_plotplotly_iterate(self):
        from unittest import mock
        from gillespy2.core.results import _plotplotly_iterate
        trajectory = Trajectory(data={'time':[0.],'foo':[1.]}, model=Model('test_model'))
        import pickle
        trajectory_unpickled = pickle.loads(pickle.dumps(trajectory))
        with mock.patch('plotly.graph_objs.Scatter') as mock_method_before_pickle:
            _plotplotly_iterate(trajectory)
        with mock.patch('plotly.graph_objs.Scatter') as mock_method_after_pickle:
            _plotplotly_iterate(trajectory_unpickled)
        assert mock_method_before_pickle.call_args_list == mock_method_after_pickle.call_args_list

    def test_to_csv_single_result_no_data(self):
        result = Results(data=None)
        test_nametag = "test_nametag"
        test_stamp = "test_stamp"

        with tempfile.TemporaryDirectory() as tempdir:
            result.to_csv(stamp = test_stamp, nametag = test_nametag, path=tempdir)
            test_path = tempdir+"/"+test_nametag+test_stamp
            assert not os.path.isdir(test_path)
            
    def test_to_csv_single_result_directory_exists(self):
        test_data = {'time':[0]}
        result = Results(data=[test_data])
        test_nametag = "test_nametag"
        test_stamp = "test_stamp"

        with tempfile.TemporaryDirectory() as tempdir:
            result.to_csv(stamp = test_stamp, nametag = test_nametag, path=tempdir)
            test_path = tempdir+"/"+test_nametag+test_stamp
            assert os.path.isdir(test_path)

    def test_to_csv_single_result_file_exists(self):
        test_data = {'time':[0]}
        result = Results(data=[test_data])
        test_nametag = "test_nametag"
        test_stamp = "test_stamp"

        with tempfile.TemporaryDirectory() as tempdir:
            result.to_csv(stamp = test_stamp, nametag = test_nametag, path=tempdir)
            test_path = tempdir+"/"+test_nametag+test_stamp+"/"+test_nametag+"0.csv"
            assert os.path.isfile(test_path)

    def test_to_csv_single_result_no_stamp(self):
        test_data = {'time':[0]}
        result = Results(data=[test_data])
        test_nametag = "test_nametag"

        with tempfile.TemporaryDirectory() as tempdir:
            result.to_csv(nametag=test_nametag, path=tempdir)
            assert len(os.listdir(tempdir)) is not 0

    def test_to_csv_single_result_no_nametag(self):
        test_model = Model('test_model')
        test_data = Trajectory(data={'time':[0]},model=test_model)
        result = Results(data=[test_data])
        result.solver_name = 'test_solver'
        test_stamp = "test_stamp"

        with tempfile.TemporaryDirectory() as tempdir:
            result.to_csv(stamp=test_stamp, path=tempdir)
            assert len(os.listdir(tempdir)) is not 0

    def test_to_csv_single_result_no_path(self):
        test_data = Trajectory({'time':[0]},model=Model('test_model'),solver_name='test_solver_name')
        result = Results(data=[test_data])
        test_nametag = "test_nametag"
        test_stamp = "test_stamp"

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            result.to_csv(stamp=test_stamp, nametag=test_nametag)
            assert len(os.listdir(tempdir)) is not 0


if __name__ == '__main__':
    unittest.main()
