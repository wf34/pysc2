import functools
import pickle
import os
import pysc2.third_party.filesystem as fs


def serialize_datum_entry(current_step, datum, file_handle):
    assert not file_handle.closed
    for object_to_store in [current_step, datum]:
        # assert object_to_store is not None
        pickle.dump(object_to_store, file_handle)


class dumper():
    """Handles incoming input data and stores it in a provided file"""
    def __init__(self, destination_folder, name):
        self.dst = destination_folder
        fs.create_dir(self.dst)
        self.name = name


    def get_dump_callback(self, replay_name, perspective):
        dst_filename = replay_name + '_' + str(perspective) + \
            '_' + self.name + '.pickle'
        f = open(os.path.join(self.dst, dst_filename), 'wb')
        return functools.partial(serialize_datum_entry, file_handle = f)


class game_dumper():
    """Store X(observations) and Y(hidden variables) in a dedicated subdir on HDD.
       We intend to train two-tailed network, where tails are:
        * match result inference
        * action inference
       The ground-truth for the hidden variables will be referenced hereafter as
       Y_uscore (ultimate score) and Y_actions respectively.

    Attributes:
      index: Index of this layer into the set of layers.
      name: The name of the layer within the set.
    """
    game_data_types = ['X', 'Y_uscore', 'Y_actions']


    def __init__(self, destination_folder):
        fs.create_dir(destination_folder)
        self.dumpers = {t : dumper(os.path.join(destination_folder, t), t) \
                        for t in self.game_data_types}


    def get_dump_callbacks(self, replay_name, perspective):
        """Provides callback function, which implement data dump

        Args:
            replay_name: hash coded unique name of a game
            perspective: player id, from whose perspective the replay was played

        Returns:
            Dict with `game_data_types` as keys and respective
            callback functions as values
        """
        return {d : d_.get_dump_callback(replay_name, perspective) \
                for d, d_ in self.dumpers.items()}

