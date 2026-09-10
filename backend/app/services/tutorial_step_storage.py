from sqlalchemy.orm import Session

from ..models import TutorialStep


def save_tutorial_steps(
    db: Session,
    video_id: int,
    steps: list[dict],
):
    db.query(TutorialStep).filter(
        TutorialStep.video_id == video_id
    ).delete(
        synchronize_session=False
    )

    saved_steps = []

    for step in steps:
        evidence = step.get(
            "evidence",
            {},
        )

        tutorial_step = TutorialStep(
            video_id=video_id,
            step_number=step["step"],
            action=step["action"],

            confidence=step.get(
                "confidence",
                0.0,
            ),

            verified=step.get(
                "verified",
                False,
            ),

            name=step.get("name"),
            path=step.get("path"),

            instruction=step["instruction"],

            start_time=step["start_time"],
            end_time=step["end_time"],

            evidence_source=evidence.get(
                "source",
                "transcript",
            ),

            evidence_text=evidence.get(
                "text",
                step["instruction"],
            ),
        )

        db.add(tutorial_step)
        saved_steps.append(tutorial_step)

    db.commit()

    return saved_steps