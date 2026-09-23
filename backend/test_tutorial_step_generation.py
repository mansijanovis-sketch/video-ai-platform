from app.services.developer_action_pipeline import (
    build_tutorial_steps,
)


def test_react_tutorial_actions_become_ordered_steps():
    segments = [
        {
            "start_time": 114.689,
            "end_time": 119.579,
            "text": "need to do MPX create react app my app",
        },
        {
            "start_time": 133.41,
            "end_time": 141.57,
            "text": "react app and I'm going to name it react tutorial",
        },
        {
            "start_time": 150.03,
            "end_time": 155.64,
            "text": "right here so we're gonna do CDU react",
        },
        {
            "start_time": 152.19,
            "end_time": 158.25,
            "text": "tutorial and then we're going to do yarn",
        },
        {
            "start_time": 152.19,
            "end_time": 160.53,
            "text": "tutorial and then we're going to do yarn start",
        },
        {
            "start_time": 1867.09,
            "end_time": 1872.57,
            "text": "can do NPM install that save reactor out",
        },
        {
            "start_time": 1869.76,
            "end_time": 1877.86,
            "text": "or Dom so let's go ahead and do that",
        },
        {
            "start_time": 1899.61,
            "end_time": 1906.0,
            "text": "code right here let's replace app dot",
        },
        {
            "start_time": 1903.03,
            "end_time": 1908.07,
            "text": "J's here save it",
        },
        {
            "start_time": 2309.81,
            "end_time": 2314.18,
            "text": "create a new file called product item",
        },
        {
            "start_time": 2387.37,
            "end_time": 2392.46,
            "text": "pascal case so product item Jas",
        },
        {
            "start_time": 2662.13,
            "end_time": 2675.79,
            "text": "let's name this file add item J s",
        },
    ]

    steps = build_tutorial_steps(segments)

    assert [(step["action"], step["path"]) for step in steps] == [
        ("run_command", "npx create-react-app react-tutorial"),
        ("run_command", "cd react-tutorial"),
        ("run_command", "yarn start"),
        ("run_command", "npm install react-router-dom"),
        ("edit_file", "App.js"),
        ("create_file", "ProductItem.js"),
        ("create_file", "AddItem.js"),
    ]
    assert [step["step"] for step in steps] == list(range(1, 8))
    assert all(step["evidence"]["text"] for step in steps)
