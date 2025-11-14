def run_pipeline(text):
    summary = (
        "• Meeting discussed upcoming product launch.\n"
        "• Team aligned on deadlines and roles.\n"
        "• Major blockers were identified.\n"
    )

    action_items = [
        {"assignee": "Rahul", "deadline": "Monday", "task": "Prepare launch mockups"},
        {"assignee": "Aisha", "deadline": "Tomorrow", "task": "Confirm vendor pricing"},
        {"assignee": "Team Lead", "deadline": "Friday", "task": "Finalize communication plan"}
    ]

    return summary, action_items
