from media_organizer.planner import Planner

def test_planner_init():
    config = {}
    planner = Planner(config)
    assert isinstance(planner, Planner)

def test_planner_plan():
    config = {}
    planner = Planner(config)
    metadata = {
        "original_path": "test/song.mp3",
        "filename": "song.mp3"
    }
    plan = planner.plan(metadata)
    assert plan["source"] == "test/song.mp3"
    # The default behavior for unknown/no template is now "Unsorted/filename"
    assert plan["destination"] == "Unsorted/song.mp3"
