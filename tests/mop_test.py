from pathlib import Path

import pytest

from mop.mop import Collector, Mop

FIXTURES_DIR = Path(__file__).parent.joinpath('fixtures')


@pytest.mark.parametrize("extensions,recursive,exclude,file_count_expected", [
    ([".jpg"], False, False, 1),
    ([".jpg", ".mp3", ".pdf"], False, False, 3),
    ([".jpg", ".mp3", ".pdf"], True, False, 11),
    ([".jpg", ".mp3", ".pdf"], False, True, 0),
    ([".jpg", ".mp3", ".pdf"], True, True, 6),
])
def test_collector(extensions, recursive, exclude, file_count_expected):
    collector = Collector(extensions=extensions, recursive=recursive, exclude=exclude)

    files = collector(path=FIXTURES_DIR)

    assert file_count_expected == len(files)


def test_mop(mocker):
    unlink = mocker.patch("pathlib.Path.unlink")
    mop = Mop(dir_path=str(FIXTURES_DIR), extensions=[".mp3"], recursive=True, exclude=False)

    files_to_delete_count = mop.files_to_delete_count
    mop.clean()

    assert unlink.call_count == files_to_delete_count
